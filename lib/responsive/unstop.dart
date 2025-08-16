import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// --- MAIN OPPORTUNITY VIEWER WIDGET ---
class OpportunityViewer extends StatefulWidget {
  const OpportunityViewer({Key? key}) : super(key: key);

  @override
  _OpportunityViewerState createState() => _OpportunityViewerState();
}

class _OpportunityViewerState extends State<OpportunityViewer> {
  List<dynamic> opportunities = [];
  List<dynamic> filteredOpportunities = [];
  bool isLoading = true;
  String? errorMessage;
  final TextEditingController searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchOpportunities();
    searchController.addListener(_filterOpportunities);
  }

  Future<void> fetchOpportunities() async {
    // A small delay to simulate network latency and show the loader
    await Future.delayed(const Duration(milliseconds: 500));
    try {
      // Use emulator loopback: http://10.0.2.2:5000/
      final response = await http.get(Uri.parse('http://10.0.2.2:5000/api/opportunities'));

      if (response.statusCode == 200) {
        setState(() {
          opportunities = json.decode(response.body);
          filteredOpportunities = opportunities;
        });
      } else {
        setState(() {
          errorMessage = 'Failed to load data. Status: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        // Provide a more user-friendly error message
        errorMessage = 'Could not connect to the server. Please check your connection.';
        debugPrint('Error fetching data: $e'); // For developer logs
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void _filterOpportunities() {
    final query = searchController.text.toLowerCase();
    setState(() {
      filteredOpportunities = opportunities.where((item) {
        // Safe access to data with null checks
        final title = (item['title'] as String?)?.toLowerCase() ?? '';
        final org = (item['organization'] as String?)?.toLowerCase() ?? '';
        final tags = (item['tags'] as String?)?.toLowerCase() ?? '';
        final category = (item['category'] as String?)?.toLowerCase() ?? '';
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
    // This widget no longer returns a Scaffold. It returns the content directly.
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (errorMessage != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            errorMessage!,
            style: TextStyle(color: Theme.of(context).colorScheme.error),
            textAlign: TextAlign.center,
          ),
        ),
      );
    }

    // Main content layout with Search Bar + List
    return Column(
      children: [
        // --- Redesigned Search Bar ---
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: TextField(
            controller: searchController,
            decoration: InputDecoration(
              hintText: 'Search opportunities...',
              prefixIcon: const Icon(Icons.search),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12.0),
                borderSide: BorderSide(color: Theme.of(context).colorScheme.primary),
              ),
              filled: true,
              fillColor: Theme.of(context).colorScheme.surface,
            ),
          ),
        ),
        // --- List of Opportunities ---
        Expanded(
          child: filteredOpportunities.isEmpty
              ? const Center(child: Text("No matches found"))
              : ListView.builder(
                  itemCount: filteredOpportunities.length,
                  itemBuilder: (context, index) {
                    final item = filteredOpportunities[index];
                    return OpportunityCard(item: item);
                  },
                ),
        ),
      ],
    );
  }
}

// --- OPPORTUNITY CARD WIDGET (for cleaner code) ---
class OpportunityCard extends StatelessWidget {
  const OpportunityCard({Key? key, required this.item}) : super(key: key);
  final Map<String, dynamic> item;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      elevation: 3.0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
      child: InkWell(
        borderRadius: BorderRadius.circular(12.0),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => OpportunityDetailPage(opportunity: item),
            ),
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                item['title'] ?? 'No Title',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Icon(
                    Icons.business_center,
                    size: 16,
                    color: Theme.of(context).textTheme.bodySmall?.color,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      item['organization'] ?? 'N/A',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}


// --- OPPORTUNITY DETAIL PAGE ---
class OpportunityDetailPage extends StatelessWidget {
  final Map<String, dynamic> opportunity;

  const OpportunityDetailPage({Key? key, required this.opportunity}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // The AppBar now correctly uses the app's theme.
      appBar: AppBar(
        title: Text(opportunity['title'] ?? 'Details'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              opportunity['title'] ?? 'No Title',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            const Divider(),
            DetailListItem(
              icon: Icons.business_center,
              title: "Organization",
              value: opportunity['organization'] ?? 'N/A',
            ),
            DetailListItem(
              icon: Icons.category,
              title: "Category",
              value: opportunity['category'] ?? 'N/A',
            ),
            DetailListItem(
              icon: Icons.local_offer,
              title: "Tags",
              value: opportunity['tags'] ?? 'N/A',
            ),
            DetailListItem(
              icon: Icons.timer_off,
              title: "Deadline",
              value: opportunity['deadline'] ?? 'N/A',
            ),
          ],
        ),
      ),
    );
  }
}

// --- DETAIL LIST ITEM (for cleaner code on detail page) ---
class DetailListItem extends StatelessWidget {
  const DetailListItem({
    Key? key,
    required this.icon,
    required this.title,
    required this.value,
  }) : super(key: key);

  final IconData icon;
  final String title;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Theme.of(context).colorScheme.primary, size: 24),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 4),
                Text(value, style: Theme.of(context).textTheme.bodyLarge),
              ],
            ),
          ),
        ],
      ),
    );
  }
}