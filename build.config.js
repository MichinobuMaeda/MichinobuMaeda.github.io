export default {
  // Source directory for MarkDown files. Default: "./docs"
  source: "./docs",
  // Target directory for HTML files. Default: "./_site"
  target: "./_site",
  // Template directory for Mustache templates and Tailwind CSS. Default: "./template"
  template: "./template",
  // Input CSS file for Tailwind CSS. Default: "input.css"
  inputCss: "input.css",
  // Output CSS file. Default: "main.css"
  outputCss: "main.css",
  // Layout file of Mustache templates. Default: "layout.html"
  layout: "layout.html",
  // Description length. Default: 160
  descriptionLength: 160,
  // Default title for items without a title. Default: "No Title"
  noTitle: "No Title",
  // Default updated_at value for items without an update date. Default: "Unknown"
  unknownUpdatedAt: "Unknown",
  // Count of last updates to show. Default: 5
  lastUpdatesCount: 5,
  // Root path of the site. Default: "/"
  root: "/",
  resources: ["img", "js", "favicon.ico"],
  categories: [
    { path: "t", name: "工作室" },
    { path: "l", name: "厚生部" },
    { path: "p", name: "政治局" },
  ],
};
