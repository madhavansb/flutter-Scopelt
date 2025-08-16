
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

class MobileScaffold extends StatelessWidget {
  final VoidCallback toggleTheme;

  const MobileScaffold({Key? key, required this.toggleTheme}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Check the current brightness to decide the icon
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      // Use the new, theme-aware AppBar function from constants
      appBar: buildAppBar(
        context: context,
        actions: [
          IconButton(
            icon: Icon(isDarkMode ? Icons.light_mode : Icons.dark_mode),
            tooltip: 'Toggle Theme', // Good for accessibility
            onPressed: toggleTheme,
          ),
        ],
      ),
      // The background color is now handled by the theme
      drawer: myDrawer,
      body: OpportunityViewer(),
    );
  }
}