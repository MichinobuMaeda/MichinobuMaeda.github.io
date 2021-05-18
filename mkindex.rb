#!/usr/bin/env ruby
require 'set'
require 'yaml'

# get configuration.
conf = YAML.load_file('mkindex.yml')

conf['sections'].each do |section|

  # get timestamp, title and tags of each pages.
  indexes = Array.new
  tag_cloud = Hash.new
  Dir["#{section}/**/*.md"].each do |md|
    next if /index\.md$/.match(md)
    title = nil
    updated = nil
    tags = nil
    File.open(md).read.gsub(/\r\n?/, "\n").each_line do |line|
      title ||= !title && line.gsub(/^#\ +/, '').strip
      updated ||= !updated && /^Update:/.match(line) && line.gsub(/^Update:\ +/, '').gsub(/unknown/, '----------').strip
      tags ||= /^Tag:/.match(line) && line.gsub(/^Tag:+/, '').strip.downcase
    end
    indexes.push("- #{updated} [#{title}](#{md[(section.length + 1) ... -3]}.html#{(tags && tags.length > 0) ? " \"#{tags}\"" : ''})")

    # count up each tag.
    tags && tags.split(/\s+/).each do |tag|
      tag_cloud[tag] = (tag_cloud[tag] || 0) + 1
    end
  end

  # generte index.html.
  lines =  Array.new
  skip = false

  # read old index.html.
  trg = File.join(section, 'index.md')
  File.open(trg).read.gsub(/\r\n?/, "\n").each_line do |line|
    line.strip!

    # insert indexes.
    if line == conf['index']['end']
      skip = false
      lines.push(line)
    elsif skip
      # ignore old indexes.
    elsif line == conf['index']['start']
      skip = true
      lines.push(line)
      lines.push('<p id="tag-cloud">')
      tag_cloud.keys.sort.each do |tag|
        lines.push("<a id=\"tag-#{tag}\" style=\"font-size: #{0.9 + Math.log10(tag_cloud[tag]) / 2}em\" href=\"javascript:filterByTag('#{tag}')\">#{tag}</a>")
      end
      lines.push('</p>')
      if tag_cloud.keys.length
        lines.push("<p><a id=\"tag-ALL\" href=\"javascript:filterByTag('ALL')\">#{conf['tags']['filterOff']}</a></p>")
      end
      lines.concat(indexes.sort { |x, y| y <=> x})
    else
      lines.push(line)
    end
  end

  # write index.html.
  File.open(trg, 'w') {|f| f.write lines.join("\n")}
end
