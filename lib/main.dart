import 'package:flutter/material.dart';
import 'package:hackathon/constants.dart'; // Import constants for the color scheme
import 'package:hackathon/responsive/desk_scaff.dart';
import 'package:hackathon/responsive/mob_scaff.dart';
import 'package:hackathon/responsive/responsive_layout.dart';
import 'package:hackathon/responsive/tab_scaff.dart';

void main() {
  runApp(MainApp());
}

class MainApp extends StatefulWidget {
  const MainApp({Key? key}) : super(key: key);

  @override
  _MainAppState createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  ThemeMode _themeMode = ThemeMode.light;

  void _toggleTheme() {
    setState(() {
      _themeMode =
          _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      // --- Light Theme Definition ---
      theme: ThemeData(
        brightness: Brightness.light,
        colorScheme: ColorScheme.fromSwatch(
          primarySwatch: primaryBlue,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      // --- Dark Theme Definition ---
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSwatch(
          primarySwatch: primaryBlue,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: _themeMode,
      home: ResponsiveLayout(
        // Pass the toggle function to all scaffolds
        mobileScaffold: MobileScaffold(toggleTheme: _toggleTheme),
        tableScaffold: TableScaffold(toggleTheme: _toggleTheme),
        // Remember to update DesktopScaffold as well
        desktopScaffold: DesktopScaffold(toggleTheme: _toggleTheme),
      ),
    );
  }
}