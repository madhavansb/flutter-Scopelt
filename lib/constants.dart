


import 'package:flutter/material.dart';

// --- Color Palette ---
// Using a consistent color palette improves UI/UX.
// This is a professional and friendly blue swatch.
const MaterialColor primaryBlue = MaterialColor(
  _bluePrimaryValue,
  <int, Color>{
    50: Color(0xFFE3F2FD),
    100: Color(0xFFBBDEFB),
    200: Color(0xFF90CAF9),
    300: Color(0xFF64B5F6),
    400: Color(0xFF42A5F5),
    500: Color(_bluePrimaryValue),
    600: Color(0xFF1E88E5),
    700: Color(0xFF1976D2),
    800: Color(0xFF1565C0),
    900: Color(0xFF0D47A1),
  },
);
const int _bluePrimaryValue = 0xFF2196F3;

// --- App Bar ---
// This function creates an AppBar that respects the app's theme.
// The title is added for better context.
AppBar buildAppBar({
  required BuildContext context,
  List<Widget>? actions,
  String title = "Opportunity Hub",
}) {
  return AppBar(
    title: Text(
      title,
      style: TextStyle(
        fontWeight: FontWeight.bold,
        color: Theme.of(context).colorScheme.onPrimary,
      ),
    ),
    backgroundColor: Theme.of(context).colorScheme.primary,
    elevation: 4.0, // Adds a subtle shadow for depth
    actions: actions,
    iconTheme: IconThemeData(color: Theme.of(context).colorScheme.onPrimary),
  );
}

// --- Drawer ---
// Updated with a more modern look and feel.
// It uses theme colors, so it will look good in both light and dark mode.
var myDrawer = Drawer(
  child: Column(
    children: [
      const UserAccountsDrawerHeader(
        accountName: Text(
          "User Name",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        accountEmail: Text("user.email@example.com"),
        currentAccountPicture: CircleAvatar(
          backgroundImage: NetworkImage(
              'https://i.pravatar.cc/150?img=12'), // A placeholder image
        ),
        decoration: BoxDecoration(
          color: primaryBlue,
        ),
      ),
      Expanded(
        child: ListView(
          padding: EdgeInsets.zero,
          children: const [
            ListTile(
              leading: Icon(Icons.dashboard_rounded),
              title: Text("D A S H B O A R D"),
            ),
            ListTile(
              leading: Icon(Icons.settings_rounded),
              title: Text("S E T T I N G S"),
            ),
          ],
        ),
      ),
    ],
  ),
);

