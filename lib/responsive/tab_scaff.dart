import 'package:flutter/material.dart';
import 'package:hackathon/constants.dart';
import 'package:hackathon/responsive/unstop.dart';

class TableScaffold extends StatefulWidget {
  const TableScaffold({super.key});

  @override
  State<TableScaffold> createState() => _TableScaffoldState();
}

class _TableScaffoldState extends State<TableScaffold> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // backgroundColor: Colors.pink,
      appBar: myAppBar,
      backgroundColor: defaultbackground,
      drawer: myDrawer,
      body:OpportunityViewer(),
    );
  }
}