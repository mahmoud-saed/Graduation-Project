import 'dart:io';
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Skin Cancer Detection',
      theme: ThemeData(

        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'upload a picture'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({key, required this.title});


  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  File? image;
  Future pickImage() async {
    try {
      final image = await ImagePicker.platform.getImage(source: ImageSource.gallery);

      if(image == null) return;

      final imageTemp = File(image.path);

      setState(() => this.image = imageTemp,);
    }
    on PlatformException catch(e) {
      print('Failed pick image: $e');
    }
  }
  @override
  Widget build(BuildContext context)
  {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('upload an image'),
      ),
      body: Center(
        child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            mainAxisSize: MainAxisSize.min,
            children: [
              MaterialButton(
                color: Colors.blue,
                child: const Text('detect',
                    style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold)
                ),
                onPressed: () {
                  pickImage();
                },
              ),
              const SizedBox(height: 20,),
              image != null ? Image.file(image!): const Text("no image selected"),
              MaterialButton(
                color: Colors.blue,
                child: const Text('upload from gallery',
                    style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold)
                ),
                onPressed: () {
                  pickImage();
                },
              ),
              MaterialButton(
                color: Colors.blue,
                child: const Text(' take a picture now ',
                    style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold)
                ),
                onPressed: () async {
                  final image = await ImagePicker.platform.getImage(source: ImageSource.camera);
                  if(image == null) return;

                  final imageTemp = File(image.path);

                  setState(() => this.image = imageTemp,);
                },
              ),

            ]),
      ),
    );
  }
}
