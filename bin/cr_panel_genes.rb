###!/usr/bin/env/ ruby
require 'mongo'
include Mongo

#make bedfile of targets for specific panel
panel_name = "episeektriome_v2"

dbname = "CR"
hosts = ["172.16.10.55:27017", "172.16.20.55:27017", "172.16.20.56:27017"]
collection = "project_types"

$mdb_ptype = Mongo::MongoReplicaSetClient.new(hosts)[dbname][collection]

criteria = {:_id=>panel_name}
attribs = ['targets']

rec = $mdb_ptype.find_one(criteria, fields: attribs)

if rec.nil?
  message = "ERROR: no record with id " + panel_name
  puts message
  exit
end

targets = rec['targets']

targets.each do |target|
	line = "chr" + target["chr"].to_s + "\t" + target["start"].to_s + "\t" + target["end"].to_s + "\t" + target["hugogene"] + "::" + target['_id'] + "\t0\n"
	print line
end

