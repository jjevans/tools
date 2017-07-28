#!/usr/bin/env ruby
require 'mongo'
include Mongo

#fetch primers for a variant and prioritize them

$DB = Mongo::MongoReplicaSetClient.new(["172.16.10.55:27017", "172.16.20.55:27017", "172.16.20.56:27017"], :read => :primary_preferred).db("CR")

  def select_primer(primers)
    return primers.first if primers.length==1  # if only 1 primer, our decision is easy
    
    #only provide primers labelled 'retire' in mdb doc
    retired = primers.select do |primer|
    	primer["retire"] == false
    end
p "#{retired} retired"
    if retired.empty?#all retired
    	return
    elsif unretired.length == 1#1 left
    	return retired.first
    else
    	primers = retired
    end
 
    #change 'success' to 'successes' as found in collection jje 04282016
    #    primers.sort_by{|z| z[:success].to_i/(z[:failures] && z[:failures].to_i>0 ? z[:failures] : 0.000001)} # sort based on success/failure ratio
    primers.sort_by{|z| z[:successes].to_i/(z[:failures] && z[:failures].to_i>0 ? z[:failures] : 0.000001)} # sort based on success/failure ratio
    primers.first                              
  end

=begin
variant = {:pos=> 108697681, :chr=>"1"}
    q={
      :genomewidehits=> {"$lte" => 1}, 
      :sense_start=> {"$lte"=> variant[:pos]-10}, 
      :end=> {"$gte"=> variant[:pos]+10}, 
      :chr=> variant[:chr]
    }
=end
pvcf = {
	:genomewidehits=> {"$lte" => 1}, 
      :sense_start=> {"$lte"=> variant[:pos]-10}, 
      :end=> {"$gte"=> variant[:pos]+10}, 
      :chr=> variant[:chr]
}


$DB['panelvcf'].find(pvcf).each do |variant|
$DB['sanger_primers_v2'].find(q).each do |primers|
	pair = select_primer(primers)
puts "#{pair['_id'].to_s}\t#{pair['retired']}\t#{pair['successes']}\t#{pair['failures']}"
end
#pair = select_primer(primers)

#p pair.to_s

exit

#response.each do |res|
#	puts res
#end

=begin
	@limit = 0
	@flds = ["_id", "chr", "start", "end", "successes", "failures"]
	@nilstr = "none"
	
	#$DB['sanger_primers_v2'].find({"_id"=> id}, :fields => @flds).limit(@limit).each do |response|
	#$DB['sanger_primers_v2'].find({}, :fields => @flds).limit(25).each do |response|
	$DB['sanger_primers_v2'].find_one()
		@answer = Array.new
		#@fldvals = ["id"=>response["_id"]]
		@fldvals = []
		
		@response.each do |res|
			#@content = response[fld].nil? ? @nilstr : response[fld]
			@fldvals.push(res)
		end
		@answer.push(@fldvals)
	#end
			
	@answer.each do |ans|
		puts ans.join('\t')
	end
=end
=begin
	@chr = 22
	@pos = 32198751
	@limit = 0
	#@flds = ["chr", "start", "end", "successes", "failures"]
	@flds = ["successes", "failures"]
	@nilstr = "none"
	@answer = Array.new
	#$DB['sanger_primers_v2'].find({}, :fields => @flds).limit(@limit).each do |response|
	$DB['sanger_primers_v2'].find({}, :fields => @flds).limit(@limit).each do |response|
	#@filts = {"chr"=> @chr, "start"=> {"$lt"=> @pos}, "end"=> {"$gt"=> @pos}}	
		#@fldvals = ["id"=>response["_id"]]
	#@primers = $DB['sanger_primers_v2'].find(@filts).each do |response|
		@fldvals = []
		puts response.to_a.join("\t")
		@flds.each do |fld|
			@content = response[fld].nil? ? @nilstr : response[fld]
			@fldvals.push(@content)
		end
		@answer.push(@fldvals)
	end
	
	@answer.each do |ans|
		puts ans.join("\t")
	end
		
	@answer.each do |ans|
		puts ans.join("\t")
	end
=end
