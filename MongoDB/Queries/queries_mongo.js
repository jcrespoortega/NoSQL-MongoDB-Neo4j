use PracticaDDBB

#CREAMOS LOS INDICES
db.publicaciones.createIndex( { "author": 1} )
db.publicaciones.createIndex( { "author.#text":1 } )

db.autores.createIndex( { "nombre": 1 } )
db.publicaciones.createIndex({“type”:1,”year”:1})
db.autores.createIndex( { "num_publicaciones": 1 } )


#CONSULTA 1
db.publicaciones.find({$or: [{"author.#text":"Walter Vogler"}, {"author":"Walter Vogler"} ] },{title:1,_id:0,year:1,type:1}).pretty()



#CONSULTA 2
db.autores.find({"nombre": "Walter Vogler"},{_id:0,nombre:1,num_publicaciones:1})

#Sin precalculos
db.publicaciones.aggregate(
[
	{$match:{author:"Walter Vogler"}},
	{$count:"author"}
])


#CONSULTA 3
db.publicaciones.find({$and: [{"type":"article"}, {"year":"2017"} ] }).count()



#CONSULTA 4
db.autores.find({"num_publicaciones": {$lt:5} }).count()

# Sin precalculo, la diferencia de tiempo es muy grande
db.autores.aggregate(
[
	{$project:{
		nombre:1,
		publicaciones:{$size:"$publicaciones"}
	}},
	{$match:{publicaciones:{$lt:5}}},
	{$count: "author"}  
])


   
   
#CONSULTA 5
db.autores.aggregate( [
	{$sort : {num_publicaciones : -1}},
	{$limit : 10},
	{$unwind:"$publicaciones"},
	{$project:{
			_id:0,
			nombre:1,
			articles:  {$sum: { $cond: [ { $eq: [ "$publicaciones.tipo", "article" ] } , 1, 0 ] }},
			inproceedings:  {$sum: { $cond: [ { $eq: [ "$publicaciones.tipo", "inproceedings" ] } , 1, 0 ] }}
		} 
	},
	{$group:{
			_id : "$nombre" ,  
			totalArticles : {$sum : "$articles" },
			totalInproceedings : {$sum :  "$inproceedings" }
		}
	}
] )
	
#Sin precalculos, el tiempo aumenta considerablemente

db.publicaciones.aggregate([
	{$project:{
		author: 1,
		type: 1}
	},
	{$unwind: "$author"},
	{$match:{
		type: {$in: ['article', 'inproceedings']}}},
	{$group:{
		_id: {
		autor: "$author",
		tipo: "$type"},
		publicaciones: {
			$sum: 1}}},
	{$group:{
		_id: {
		autor: "$_id.autor",},
		publicaciones: {
		$push:{
		"tipo": "$_id.tipo",
		"cantidad": "$publicaciones"}},
		total: {$sum: "$publicaciones"}}},
	{$sort: {"total": -1}},
	{$limit: 10}
	],
	{
		allowDiskUse:true
	})



#CONSULTA 6
db.publicaciones.aggregate([
	{$project: {
		type: 1,
		num_autores: {$cond: [ { $eq: [ { $type: "$author"}, "array" ] } , { $size: "$author" } , 1]}
		}
	},
	{$group:{
			_id : null ,
			media_autores:{$avg: "$num_autores"}
		}
	}
])

#CONSULTA 7
db.publicaciones.aggregate([
	{$match: {author : "Walter Vogler"} },
	{$unwind:"$author"},
	{$project:{author:1,"@key":1} },
	{$group : 
		{  
			_id : "@key",  
			coautores : {$addToSet : "$author"} 
		}
	},
	{$unwind:"$coautores"},
	{$match: { coautores : {$ne: "Walter Vogler"} } },
	{$project:{
		coautores:1,
		_id:0} 
	},
	{$sort: {coautores:1}}
])

#CONSULTA 8
db.autores.aggregate( [
		{$sort : {edad : -1}},
		{$limit : 5},
		{$project:{nombre:1,edad:1,_id:0} }
	] )


#CONSULTA 9
db.autores.find({edad: {$lt: 5 }}).count()

#Sin precalculos
db.publicaciones.aggregate([
	{$project:{
		author: 1,
		year: 1}},
	{$unwind: "$author"},
	{$group:{
		_id: "$author",
		edad_max: {$max: "$year"},
		edad_min: {$min: "$year"}}},
	{$addFields:{edad:{
					$subtract: ["$edad_max","$edad_min"]}}},
	{$project:{edad:1}},
	{$match:{
		edad:{
			$lt: 5}}}, 
	{$count: "numero_autores_novatos"}
], 
{
	allowDiskUse:true
})

#CONSULTA 10
var total_revistas = db.publicaciones.find({"type":"article"}).count()
var total_publicaciones = db.publicaciones.find().count()
var porcentaje = (total_revistas/total_publicaciones)*100