#!/usr/bin/env ruby
require 'netsuite_utils.rb'

#run method NS_get_basic to run script in netsuite
#jje, jw 01152016
do_call = true#dry run=false
do_print = false#print args
do_header = false

type = "get"
deploy = 1
#p = {'script'=>342,(opt) 'type'=>'get',(opt) 'data'=>{'id'=>'5456',pt=>['213','335']}}

#usage
if ARGV.length == 0
	message = "usage:\tns_get_fields_multi.rb rectype id=id0,id1,id2 fld0 fld1 fld2\n\t\twhere id is a comma separated list of ids\n\t\tfields (fld0) is a field name to output"
	abort(message)
end

#args
rectype = ARGV.shift

ids = Array.new
fields = Array.new

ARGV.each do |arg|
	argarr = arg.split(/=/)
	
	if argarr[0] == "id"
		ids = argarr[1].split(',')
	
	elsif argarr.length == 1#fields to output
		fields.push(argarr[0])
	end
end


args = {"rt".to_sym=>rectype, "id".to_sym=>ids, "flds".to_sym=>fields}

#print args
if do_print
	puts args
end

#run it
if do_call
	response = NS_get_fields_multi(args)
	
	if !response.nil?
		if do_header
			puts fields.join("\t")
		end
		
		response.each do |record|
			output = Array.new

			fields.each do |field|
				output.push(record[field])
			end
			
			puts "#{output.join("\t")}"
		end
	else
		puts "nil: netsuite response empty."
	end
end

exit

=begin
 # q[:id] = ["6420","1039"] or q[:id] = "6420"
  # q[:flds] = ["custrecord_p_first_name","custrecord_p_last_name"]
  # q[:rt] = "customrecord_patient"
=end
