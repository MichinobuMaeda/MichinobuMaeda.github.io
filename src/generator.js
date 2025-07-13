import { join, resolve, relative, dirname } from "node:path";
import { existsSync } from "node:fs";
import {
  cp,
  rm,
  mkdir,
  glob,
  lstat,
  copyFile,
  readFile,
  writeFile,
} from "node:fs/promises";
import { exec } from "node:child_process";
import { promisify } from "node:util";
import { marked } from "marked";
import Mustache from "mustache";

const execAsync = promisify(exec);
marked.use({
  gfm: true,
});
const year = new Date().getFullYear();

export class Generator {
  /**
   * @param {object} conf
   */
  constructor({
    source,
    target,
    template,
    inputCss,
    outputCss,
    layout,
    descriptionLength,
    noTitle,
    unknownUpdatedAt,
    root,
    lastUpdatesCount,
    categories,
    resources,
  }) {
    this.target = target || "./_site";
    this.source = source || "./docs";
    this.template = template || "./template";
    this.inputCss = inputCss || "input.css";
    this.outputCss = outputCss || "main.css";
    this.layout = layout || "layout.html";
    this.descriptionLength = descriptionLength || 160;
    this.noTitle = noTitle || "No Title";
    this.unknownUpdatedAt = unknownUpdatedAt || "Unknown";
    this.root = root || "/";
    this.lastUpdatesCount = lastUpdatesCount || 5;
    this.categories = categories || [];
    this.resources = resources || [];
    this.pages = {};
  }

  /**
   * Generate the project.
   * This method orchestrates the entire build process,
   * including cleaning the target directory,
   * generating CSS, and processing Markdown files.
   *
   * @returns {Promise<void>}
   */
  async generate() {
    console.log("Building the project...");

    await this.clean();
    await Promise.all([
      this.generateCss(),
      this.getAllSourceFiles().then(({ md, media }) =>
        Promise.all([
          this.generateMetaData(md).then((metaData) =>
            Promise.all([
              this.outputHtmlPages(metaData),
              this.writeCategoriesIndex(metaData),
            ]),
          ),
          this.copyMediaFiles(media),
        ]),
      ),
      this.copyResources(),
    ]);

    console.log("Completed building the project!");
  }

  /**
   * Clean up target dir.
   *
   * @returns {Promise<void>}
   */
  async clean() {
    if (existsSync(this.target)) {
      await rm(this.target, { recursive: true });
    }
    await mkdir(this.target, { recursive: true });
  }

  /**
   * Generate css in target dir.
   *
   * @returns {Promise<void>}
   */
  async generateCss() {
    console.info("Start: Generate css");
    const inputCss = join(this.template, this.inputCss);
    const outputCss = join(this.target, this.outputCss);
    await execAsync(`npx tailwindcss -i ${inputCss} -o ${outputCss}`);
    console.info("End  : Generate css");
  }

  /**
   * Get all files path from source dir.
   *
   * @returns {Promise<object>} - An object containing arrays of Markdown and media file paths.
   */
  async getAllSourceFiles() {
    console.info("Start: Get all source files path");
    const md = [];
    const media = [];
    const dirs = [];

    for await (const entry of glob(`${this.source}/**/*`)) {
      if ((await lstat(entry)).isFile()) {
        const dir = dirname(join(this.target, relative(this.source, entry)));
        if (!dirs.includes(dir)) {
          if (!existsSync(dir)) {
            await mkdir(dir, { recursive: true });
          }
          dirs.push(dir);
        }
        if (entry.endsWith(".md")) {
          md.push(entry);
        } else {
          media.push(entry);
        }
      }
    }
    console.info("End  : Get all source files path");
    return { md, media };
  }

  /**
   * Generate HTML files from Markdown files.
   *
   * @param {Array<string>} paths - Array of Markdown file paths.
   * @returns {Promise<void>}
   */
  async generateMetaData(paths) {
    console.info("Start: Generate metadata from Markdown files");
    const metaData = (
      await Promise.all(paths.map((path) => this.parseMarkdown(path)))
    )
      .map((item) => ({
        ...item,
        updated_at: item.updated_at.replace(/-/g, "/"),
      }))
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at))
      .map((meta) => ({
        ...meta,
        updated_at: meta.updated_at || this.unknownUpdatedAt,
      }));
    console.info("End  : Generate metadata from Markdown files");
    return metaData;
  }

  /**
   * Parse a markdown file.
   *
   * @returns {Promise<object>}
   */
  async parseMarkdown(path) {
    const category = this.resolveCategory(path);
    const meta = {
      cat: category ? category.path : null,
      path: relative(this.source, path).replace(/\.md/i, ".html"),
      title: null,
      description: "",
      updated_at: "",
      tags: null,
    };

    const dir = dirname(relative(this.source, path));
    if (!existsSync(join(this.target, dir))) {
      await mkdir(join(this.target, dir), { recursive: true });
    }

    const md = await readFile(resolve(path), { encoding: "utf8" });
    let isTitleLine = false;

    md.split("\n").forEach((line) => {
      if (category) {
        if (!meta.title && line.trim()) {
          meta.title = line.trim();
        }
        if (!isTitleLine && /^#\s+/.test(line)) {
          meta.title = line.replace(/^#\s+/, "").trim();
          isTitleLine = !!meta.title;
        } else if (!isTitleLine && /^##\s+/.test(line)) {
          meta.title = line.replace(/^##\s+/, "").trim();
          isTitleLine = !!meta.title;
        } else if (!meta.updated_at && /^Update:\s*/i.test(line)) {
          meta.updated_at = line
            .replace(/^Update:\s*/i, "")
            .replace(/[^0-9/-]+/, "")
            .trim();
        } else if (/^Tag:\s*/i.test(line)) {
          meta.tags = line
            .replace(/^Tag:\s*/i, "")
            .trim()
            .split(/\s+/)
            .filter((tag) => tag)
            .map((tag) => tag.toLowerCase());
        } else if (meta.description.length < this.descriptionLength) {
          meta.description =
            meta.description.trim() +
            " " +
            line
              .trim()
              .replace(/#+\s+/, "")
              .replace(/<.+>/, "")
              .replace(/!*\[(.*)\]\(.+\)/, "$1");
        }

        if (!meta.title) {
          meta.title = this.noTitle;
        }
      }
    });

    if (meta.description.length > this.descriptionLength) {
      meta.description =
        meta.description.trim().substring(0, this.descriptionLength - 3) +
        "...";
    }

    this.pages[relative(this.source, path).replace(/\.md/i, ".html")] = marked
      .parse(md)
      .replace('class="language-mermaid"', 'class="mermaid nohighlight"');

    return meta;
  }

  /**
   * Copy all media files
   *
   * @param {Array<string>} media
   * @returns {Promise<void>}
   */
  async copyMediaFiles(media) {
    console.info("Start: Copy media files");
    await Promise.all(
      media.map((file) =>
        copyFile(
          resolve(file),
          resolve(join(this.target, relative(this.source, file))),
        ),
      ),
    );
    console.info("End  : Copy media files");
  }

  /**
   * Generate 'meta.json'.
   *
   * @param {Array<object>} metaData - Array of metadata objects for each Markdown file.
   * @returns {Promise<void>}
   */
  async outputHtmlPages(metaData) {
    console.info("Start: Output HTML pages");
    const layout = await readFile(join(this.template, this.layout), {
      encoding: "utf8",
    });
    const updates = this.generateLastUpdates(metaData);
    await Promise.all(
      metaData.map(async (meta) => {
        await writeFile(
          join(this.target, meta.path.replace(/\.md/i, ".html")),
          Mustache.render(layout, {
            ...meta,
            categories: this.categories,
            category: this.resolveCategory(meta.path),
            content: this.pages[meta.path],
            root: this.root,
            lastUpdatesCount: this.lastUpdatesCount,
            updates,
            year,
          }),
          { encoding: "utf8" },
        );
      }),
    );
    console.info("End  : Output HTML pages");
  }

  /**
   * Generate categories index files.
   *
   * @returns {Promise<void>}
   */
  async writeCategoriesIndex(metaData) {
    console.info("Start: Generate categories index files");
    const updates = this.generateLastUpdates(metaData);
    await Promise.all(
      this.categories.map(async (category) => {
        await writeFile(
          join(this.target, category.path, "index.html"),
          Mustache.render(
            await readFile(join(this.template, this.layout), {
              encoding: "utf8",
            }),
            {
              categories: this.categories,
              category,
              tag_cloud: {
                tag: this.generateTagCloud(metaData, category),
              },
              pages: {
                page: metaData.filter((item) => item.cat === category.path),
              },
              root: this.root,
              lastUpdatesCount: this.lastUpdatesCount,
              updates,
              year,
            },
          ),
          { encoding: "utf8" },
        );
      }),
    );
    console.info("End  : Generate categories index files");
  }

  /**
   * Generate last updates data.
   * @param {Array<object>} metaData
   * @returns {Array<object>}
   */
  generateLastUpdates(metaData) {
    console.info("Start: Generate last updates");
    const updates = metaData
      .slice(0, this.lastUpdatesCount)
      .map(({ updated_at, path, title }) => ({
        updated_at,
        path,
        title,
      }))
      .sort((a, b) => b.updated_at.localeCompare(a.updated_at));
    console.info("End  : Generate last updates");
    return updates;
  }

  /**
   * Generate tag cloud data.
   *
   * @param {Array<object>} metaData - Array of metadata objects for each Markdown file.
   * @param {object} category - The category object to filter tags by.
   * @returns {Promise<Array<object>} - An array of tag objects with name and count.
   */
  generateTagCloud(metaData, category) {
    console.info("Start: Generate tag cloud data");
    const tags = {};

    for (const item of metaData) {
      if (item.tags && item.cat === category.path) {
        for (const tag of item.tags.filter((tag) => tag)) {
          if (!tags[tag]) {
            tags[tag] = 0;
          }
          tags[tag]++;
        }
      }
    }

    const tagList = Object.entries(tags)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => a.name.localeCompare(b.name));

    console.info("End  : Generate tag cloud data");
    return tagList;
  }

  /**
   * Copy resources to target directory.
   *
   * @returns {Promise<void>}
   */
  async copyResources() {
    console.info("Start: Copy resources");
    await Promise.all(
      this.resources.map((resource) =>
        cp(
          join(resolve(this.template), resource),
          join(resolve(this.target), resource),
          {
            recursive: true,
          },
        ),
      ),
    );
    console.info("End  : Copy resources");
  }

  /**
   * Resolve category
   *
   * @returns {object|undefined}
   */
  resolveCategory(path) {
    return this.categories.find((cat) =>
      resolve(path).startsWith(resolve(join(this.source, cat.path))),
    );
  }
}
