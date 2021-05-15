require 'yaml'

conf = YAML.load_file('mkindex.yml')

conf['sections'].each do |section|
  indexes = Array.new
  Dir["#{section}/**/*.md"].each do |md|
    next if /index\.md$/.match(md)
    title = nil
    updated = nil
    File.open(md).read.gsub(/\r\n?/, "\n").each_line do |line|
      title ||= !title && line.gsub(/^#\ +/, '').strip
      updated ||= !updated && /^Update:/.match(line) && line.gsub(/^Update:\ +/, '').gsub(/unknown/, '----------').strip
    end
    indexes.push("- #{updated} [#{title}](#{md[(section.length + 1) ... -3]}.html)")
  end
  lines =  Array.new
  skip = false
  trg = File.join(section, 'index.md')
  File.open(trg).read.gsub(/\r\n?/, "\n").each_line do |line|
    line.strip!
    if line == conf['index']['end']
      skip = false
      lines.push(line)
    elsif skip
      # ignore
    elsif line == conf['index']['start']
      skip = true
      lines.push(line)
      lines.concat(indexes.sort { |x, y| y <=> x})
    else
      lines.push(line)
    end
  end
  File.open(trg, 'w') {|f| f.write lines.join("\n")}
end
