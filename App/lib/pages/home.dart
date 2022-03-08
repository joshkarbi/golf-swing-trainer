import 'package:app/data/footer_items.dart';
import 'package:app/pages/camera_screen.dart';
import 'package:app/pages/stats_screen.dart';
import 'package:flutter/material.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  int pageIndex=0;

  late Map<String,dynamic> emptyMap={};
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomSheet: getFooter(),
      body: getBody(),
    );
  }

  Widget getBody(){
    return IndexedStack(
      index: pageIndex,
      children: [
        CameraScreen(),//StatsScreen( receivedMap: emptyMap,)
      ],
    );
  }

  Widget getFooter(){
    return Container(
      width: double.infinity,
      height: 90,
      decoration: const BoxDecoration(color: Colors.black),
      child: Padding(
        padding: const EdgeInsets.only(left: 20, right: 20, bottom: 20, top: 10),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: List.generate(iconsItems.length, (index) {
           return GestureDetector(
            onTap: (){
            setState(() {
              pageIndex=index;
            });
           },
            child: Column(
              children: [
                Icon(
                  iconsItems[index],
                  color: pageIndex == index ? Colors.white : Colors.white.withOpacity(0.5)  ,
                ),
                SizedBox(
                  height: 5,
                ),
                Text(textItems[index],
                style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w500,
                    color: pageIndex == index ? Colors.white : Colors.white.withOpacity(0.5)),
                )
              ],
            )
           );
          }),
        ),
      ),
    );
  }
}
