import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class OpportunityViewer extends StatefulWidget {
  @override
  _OpportunityViewerState createState() => _OpportunityViewerState();
}

class _OpportunityViewerState extends State<OpportunityViewer> {
  List<dynamic> opportunities = [];
  List<dynamic> filteredOpportunities = [];
  bool isLoading = true;
  String? errorMessage;
  TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchOpportunities();
    searchController.addListener(_filterOpportunities);
  }

  Future<void> fetchOpportunities() async {
    try {
      final response = await http.get(
        Uri.parse('http://10.0.2.2:5000/api/opportunities'), //android emulator
        Uri.parse('http://192.168.1.10:5000/api/opportunities'), // connecting to the mobile device through the usb cable
      );

      if (response.statusCode == 200) {
        setState(() {
          opportunities = json.decode(response.body);
          filteredOpportunities = opportunities;
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Failed to load data. Status: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error fetching data: $e';
        isLoading = false;
      });
    }
  }

  void _filterOpportunities() {
    final query = searchController.text.toLowerCase();
    setState(() {
      filteredOpportunities = opportunities.where((item) {
        final title = item['title']?.toLowerCase() ?? '';
        final org = item['organization']?.toLowerCase() ?? '';
        final tags = item['tags']?.toLowerCase() ?? '';
        final category = item['category']?.toLowerCase() ?? '';
        return title.contains(query) ||
            org.contains(query) ||
            tags.contains(query) ||
            category.contains(query);
      }).toList();
    });
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: searchController,
          style: TextStyle(color: Colors.white),
          decoration: InputDecoration(
            hintText: 'Search...',
            hintStyle: TextStyle(color: Colors.white70),
            border: InputBorder.none,
            icon: Icon(Icons.search, color: Colors.white),
          ),
        ),
        backgroundColor: Colors.blueGrey,
      ),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : errorMessage != null
          ? Center(child: Text(errorMessage!, style: TextStyle(color: Colors.red)))
          : filteredOpportunities.isEmpty
          ? Center(child: Text("No matches found"))
          : ListView.builder(
        itemCount: filteredOpportunities.length,
        itemBuilder: (context, index) {
          final item = filteredOpportunities[index];
          return Card(
            margin: EdgeInsets.all(10),
            child: Padding(
              padding: EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(item['title'] ?? 'No Title',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  SizedBox(height: 4),
                  Text("Organization: ${item['organization'] ?? 'N/A'}"),
                  Text("Tags: ${item['tags'] ?? 'N/A'}"),
                  Text("Deadline: ${item['deadline'] ?? 'N/A'}"),
                  Text("Category: ${item['category'] ?? 'N/A'}"),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
