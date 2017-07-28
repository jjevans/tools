#!/usr/bin/env ruby
require 'mongo'
include Mongo

$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")

collect = $DB['sanger_tracking']

collect.find({:variants_n_primers=>{"$exists"=>true}}, fields: ['variants_n_primers', 'variants', 'updated_at', 'type']).sort({'updated_at'=>-1}).each do |gpp|
if !gpp['variants_n_primers'].nil? and gpp['variants_n_primers'].keys.length > 0
	gpp['variants_n_primers'].keys.each do |vnp|

  if gpp['variants_n_primers'][vnp].include?('reason')
      	  puts gpp["_id"]+"\t"+gpp["updated_at"].to_s+"\t"+gpp["type"].to_s+"\t"+gpp["variants_n_primers"][vnp]["reason"].to_s+"\tvnp"
	end

	end
end
end
