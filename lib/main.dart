import 'package:flutter/material.dart';
import 'package:hackathon/responsive/desk_scaff.dart';
import 'package:hackathon/responsive/mob_scaff.dart';
import 'package:hackathon/responsive/responsive_layout.dart';
import 'package:hackathon/responsive/tab_scaff.dart';

void main() {
  runApp(MainApp());
}

class MainApp extends StatelessWidget {
  // const MainApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ResponsiveLayout(
        mobileScaffold: const MobileScaffold(),
        tableScaffold: const TableScaffold(),
        desktopScaffold: const DesktopScaffold(),
      ),

    );
  }
}
