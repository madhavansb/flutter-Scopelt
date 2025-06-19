import 'package:flutter/material.dart';
import 'package:hackathon/constants.dart';
import 'package:hackathon/responsive/unstop.dart';

class MobileScaffold extends StatefulWidget {
  const MobileScaffold({super.key});

  @override
  State<MobileScaffold> createState() => _MobileScaffoldState();
}

class _MobileScaffoldState extends State<MobileScaffold> {
  @override
  Widget build(BuildContext context) {
    return  Scaffold(
      appBar: myAppBar,
      backgroundColor: defaultbackground,
      drawer: myDrawer,
      body:OpportunityViewer(),
    );
  }
}