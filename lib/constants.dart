import 'package:flutter/material.dart';

var defaultbackground=Colors.grey[300];

var myAppBar=AppBar(
  backgroundColor: Colors.grey[600],
);

var myDrawer = Drawer(
  backgroundColor: Colors.grey[600],
  child: ListView(
    padding: EdgeInsets.zero,
    children: [
      DrawerHeader(child: Icon(Icons.favorite)),
      ListTile(
        leading: Icon(Icons.home),
        title: Text("D A S H B O A R D"),
      ),
      ListTile(
        leading: Icon(Icons.settings),
        title: Text("S E T T I N G S"),
      ),
      ListTile(
        leading: Icon(Icons.logout),
        title: Text("L O G O U T"),
      ),
    ],
  ),
);
