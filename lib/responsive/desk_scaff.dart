import 'package:flutter/material.dart';
import 'package:hackathon/constants.dart';
import 'package:hackathon/responsive/unstop.dart'; // Make sure OpportunityViewer is imported

class DesktopScaffold extends StatelessWidget {
  final VoidCallback toggleTheme;

  const DesktopScaffold({Key? key, required this.toggleTheme}) : super(key: key);

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
          const SizedBox(width: 10), // Adds a bit of spacing
        ],
      ),
      // The background color is now handled by the theme
      body: Row(
        children: [
          // On desktop, the drawer is often permanently visible.
          myDrawer,

          // Main content area
          Expanded(
            child: OpportunityViewer(),
          ),
        ],
      ),
    );
  }
}