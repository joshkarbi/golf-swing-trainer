import 'dart:typed_data';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:app/main.dart';
class StatsScreen extends StatefulWidget {
  late Map<String, dynamic> receivedMap;
  StatsScreen({required this.receivedMap});
  
  @override
  State<StatsScreen> createState() => _StatsScreenState();
}

class _StatsScreenState extends State<StatsScreen> {


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.withOpacity(0.05),
      body: getBody(),
    );
  }
  /*Future<void> getMedia() async {
    final ByteData imageData = await NetworkAssetBundle(Uri.parse("http://192.168.0.32:5000/static/swing_overlay.png")).load("");
    final Uint8List bytes = imageData.buffer.asUint8List();
  }*/
  Widget getBody()  {
    /*getMedia()*/;
    final List feedbackList=[];
    final List icons=[];

    if (widget.receivedMap["pieces_of_feedback"]["arm_pos_feedback_msg"]!=null){
      feedbackList.add(widget.receivedMap["pieces_of_feedback"]["arm_pos_feedback_msg"]);
      icons.add(Icons.emoji_people);
    }
    if (widget.receivedMap["pieces_of_feedback"]["wrist_pos_feedback_msg"]!=null){
      feedbackList.add(widget.receivedMap["pieces_of_feedback"]["wrist_pos_feedback_msg"]);
      icons.add(Icons.golf_course);
    }
    if (widget.receivedMap["pieces_of_feedback"]["knee_pos_feedback_msg"]!=null){
      feedbackList.add(widget.receivedMap["pieces_of_feedback"]["knee_pos_feedback_msg"]);
      icons.add(Icons.boy);
    }
    if (widget.receivedMap["pieces_of_feedback"]["feet_pos_feedback_msg"]!=null){
      feedbackList.add(widget.receivedMap["pieces_of_feedback"]["feet_pos_feedback_msg"]);
      icons.add(Icons.do_not_step);
    }
    if (widget.receivedMap["metrics"]["ball_speed"]!=null){
      feedbackList.add("Ball Speed: ${(widget.receivedMap["metrics"]["ball_speed"]).toString()} m/s");
      icons.add(Icons.speed);
    }
    if (widget.receivedMap["metrics"]["launch_angle"]!=null){
      feedbackList.add("Launch Angle: ${(widget.receivedMap["metrics"]["launch_angle"]).toString()}°");
      icons.add(Icons.square_foot);
    }
    if (widget.receivedMap["metrics"]["carry_distance"]!=null){
      feedbackList.add("Carry Distance: ${(widget.receivedMap["metrics"]["carry_distance"]).toString()} m");
      icons.add(Icons.straighten);
    }



    return Material(
      type: MaterialType.transparency,
      child: SingleChildScrollView(
        //child: Text("Wrist : ${widget.receivedMap["pieces_of_feedback"]["wrist_pos_feedback_msg"]}")
        child: Column(
          children: [
            Container(
                decoration: BoxDecoration(color: Colors.white, boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.01),
                    spreadRadius: 10,
                    blurRadius: 3,
                    // changes position of shadow
                  ),
                ]),
                child: Padding(
                  padding: const EdgeInsets.only(
                      top: 60, right: 20, left: 20, bottom: 25),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: const [
                          Text(
                            "Swing Analysis",
                            style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.black),
                          ),
                        ],
                      ),

                      ListView.builder(
                          scrollDirection: Axis.vertical,
                          shrinkWrap: true,
                          itemCount: feedbackList.length,
                          itemBuilder: (context, index) {
                        return ListTile(
                          leading: Icon(icons[index]),
                          title: Text(feedbackList[index]),
                        );
                      }),

                      Image.network("http://192.168.0.32:5000/static/animation.gif"),

                    ],
                  ),

                )
            )
          ],
        ),
      ),
    );

  }
}
