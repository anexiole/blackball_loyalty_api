import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Loyalty Card App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _userIdController = TextEditingController();
  final _phoneNumberController = TextEditingController();
  final _passwordController = TextEditingController();
  String _errorMessage;

  Future<void> _login() async {
    String url = 'http://localhost:8000/login/';
    Map<String, String> headers = {'Content-Type': 'application/json'};
    Map<String, dynamic> body = {};

    if (_userIdController.text.isNotEmpty) {
      body['user_id'] = _userIdController.text;
    } else if (_phoneNumberController.text.isNotEmpty) {
      body['phone_number'] = _phoneNumberController.text;
    } else {
      setState(() {
        _errorMessage = 'Please provide user ID or phone number.';

