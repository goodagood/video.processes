
#

youtube_url_file   = '/tmp/yhb'
if ARGV[0]
    youtube_url_file   = ARGV[0]
end

done_video_list    = File.join(ENV["HOME"], "tmp/done-video-list")
if ARGV[1]
    done_video_list    = ARGV[1]
end

<<-comment
file_lines = []
File.open(youtube_url_file).each_line  do |line|
    file_lines << line
end
comment

#puts file_content.length

class  YoutubeDownloader

    def initialize(youtube_url_file, old_url_file)
        @youtube_url_file = youtube_url_file
        @old_url_file = old_url_file
    end

    def read_strip_lines(file_name)
        lines = []
        return lines if not File.exist?(file_name)

        File.open(file_name, "r").each_line  do |line|
            l = line.strip
            #puts l
            #lines << l
            lines.push(l)
        end
        return lines
    end


    def find_string_in_array(s, a)
        # find whether array contains string
        # s: string
        # a: array of strings
        return false if not a

        a.each do |one|
            if one == s
                # find equal, return now.
                return true
            end
        end

        # find none.
        return false
    end

    def append_line(file_name, line)
        File.open(file_name, 'a+') do |file|
            file.write(line + "\n")
        end
    end



    <<-MLSTRING
        #puts read_strip_lines(@old_url_file)
    MLSTRING

    def dojob
        src_urls = read_strip_lines(@youtube_url_file)
        old_urls = read_strip_lines(@old_url_file)


        src_urls.each do |url|
            if not find_string_in_array(url, old_urls)
                puts 'get: ' + url
                #append a line
                append_line(@old_url_file, url)
            end
        end
    end

end


yd = YoutubeDownloader.new(youtube_url_file, done_video_list)
yd.dojob
