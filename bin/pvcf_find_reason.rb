#!/usr/bin/env ruby
require 'mongo'
include Mongo
require 'time'

$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55","172.16.20.55","172.16.20.56"], :read => :primary_preferred).db("CR")

pvcf = $DB['panelvcf']

july2016 = Time.new(2016, 7)

pvcf.find({:rundate=> {"$gt"=>july2016}}, :fields=> ['variantlist', 'gpp', 'rundate']).each do |rpt|

    if !rpt["variantlist"].nil? or rpt["variantlist"].length == 0

        rpt["variantlist"].to_a.each do |variant|

            if !variant["swap"].nil? and variant["swap"].to_s !="" and variant["swap"] == true and !variant["ref"].nil? and !variant["alt"].nil? and variant["ref"] == variant["alt"]
                    puts "#{rpt['gpp']}\t#{rpt['_id']}\t#{rpt['rundate'].utc}\t#{variant['variant_id']}"
            end
        end
    end
end
=begin
collect.find({:variants_n_primers=>{"$exists"=>true}}, fields: ['variants_n_primers', 'variants', 'updated_at', 'type']).sort({'updated_at'=>-1}).each do |gpp|
if !gpp['variants_n_primers'].nil? and gpp['variants_n_primers'].keys.length > 0
	gpp['variants_n_primers'].keys.each do |vnp|

  if gpp['variants_n_primers'][vnp].include?('reason')
      	  puts gpp["_id"]+"\t"+gpp["updated_at"].to_s+"\t"+gpp["type"].to_s+"\t"+gpp["variants_n_primers"][vnp]["reason"].to_s+"\tvnp"
	end

	end
end
end
=end
