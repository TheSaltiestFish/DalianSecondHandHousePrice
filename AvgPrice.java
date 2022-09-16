package cn.itcast.spark;

import cn.itcast.dao.SparkMongoDao;
import com.google.gson.JsonObject;
import com.mongodb.spark.rdd.api.java.JavaMongoRDD;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.function.*;
import org.bson.Document;
import scala.Tuple2;
public class AvgPrice {
    public static void main(String[] args) throws InterruptedException  {
        //实例化 Spark 连接 MongoDB 对象 sparkMongoDao,通过调用
        //sperkMongoDao 对象的readFromMongoDB()方法指定并获取数据库集合中的数据－并将
        //数据放入 mongoRDD(JavaMongoRDD).
        SparkMongoDao sparkMongoDao = new SparkMongoDao();
        JavaMongoRDD<Document> mongoRDD = sparkMongoDao
                .readFromMongoDB("mongoproject","house");
        //通过 Spark 中的 mapToPair 算子对 mongoRDD进行处理，提取
        //mongoRDD 中每条房源信息中 district(房源所在区）和 unit_price(房源均价（元／平方米）
        // 两个字段数据，生成新的键值对类型 RDD(JavaPairRDD)并命名为sparkRDD,并将这两个
        //字段数据作为sparkRDD的键和值。
        JavaPairRDD<String,Integer> sparkRDD = mongoRDD.mapToPair(
                new PairFunction<Document, String, Integer>() {
                    @Override
                    public Tuple2<String, Integer> call(Document document)
                            throws Exception {
                        String regex = "\\(.*?\\)";
                        String district = document.getString("district")
                                .replaceAll(regex,"");
                        Integer unit_price = document
                                .getInteger("unit_price");
                        return new Tuple2<>(district,unit_price);
                    }
                });
        //通过Spark中的 groupByKey算子对sparkRDD进行处理，通过
        //sparkRDD 中的键（房源所在区）进行分组，生成新的键值对类型RDD(JavaPairRDD)并
        //名为 groupRDD.
        JavaPairRDD<String,Iterable<Integer>> groupRDD =
                sparkRDD.groupByKey();
        //通过Spark 中的 mapToPair 算子对 groupRDD进行处理，对相同键
        //的值进行累加处理并统计相同键中值的个数，便于后续的平均值计算，生成新的键值对类型
        //RDD(JavaPairRDD)并命名为 mapRDD.
        JavaPairRDD<Tuple2<String,Integer>,Integer> mapRDD =
                groupRDD.mapToPair(
                        new PairFunction<
                                Tuple2<String, Iterable<Integer>>,
                                Tuple2<String, Integer>, Integer>() {
            @Override
            public Tuple2<
                    Tuple2<String, Integer>,
                    Integer> call(Tuple2<String, Iterable<Integer>> tuple2)
                    throws Exception {
                int num = 0;
                int sum = 0;
                for (int i : tuple2._2) {
                    sum = sum + i;
                    num = num + 1;
                }
                Tuple2<String, Integer> tuple = new Tuple2<>(tuple2._1,sum);
                return new Tuple2<>(tuple,num);
            }
        });
        //通过Spark中的 mapToPair 算子对 mapRDD进行处理，计算得出每
        //个地区的二手房均价，生成新的键值对类型 RDD(JavaPairRDD)命名为avgRDD.
        JavaPairRDD<String,Double> avgRDD = mapRDD.mapToPair(
                new PairFunction<
                        Tuple2<Tuple2<String, Integer>, Integer>,
                        String, Double>() {
            @Override
            public Tuple2<String, Double> call(
                    Tuple2<Tuple2<String, Integer>, Integer> tuple2)
                    throws Exception {
                double sums = tuple2._1()._2.doubleValue();
                double nums = tuple2._2.doubleValue();
                double avg_price = sums/nums;
                double avg_num=(double)(Math.round(avg_price*100))/100;
                return new Tuple2<>(tuple2._1()._1,new Double(avg_num));
            }
        });
        //通过Spark中的map算子对avgRDD进行处理，将拆分键值对数据
        //并组合成json形式，便于后续通过Spark将分析结果存储到MongoDB数据库中，生成新的
        //RDD(JavaRDD)并命名为 resultRDD
        JavaRDD<Document> resultRDD = avgRDD.map(
                new Function<Tuple2<String, Double>, Document>() {
            @Override
            public Document call(Tuple2<String, Double> tuple2)
                    throws Exception {
                JsonObject resultJson = new JsonObject();
                resultJson.addProperty("district",tuple2._1);
                resultJson.addProperty("avg_price",tuple2._2);
                Document.parse(resultJson.toString());
                return  Document.parse(resultJson.toString());
            }
        });
        //通过调用sparkMongoDao对象的writeToMongoDB方法将分析结
        //果存储到MongoDB数据库中。
        sparkMongoDao.writeToMongoDB(
                "mongoproject",
                "avgprice",
                resultRDD);
        sparkMongoDao.close();
    }
}