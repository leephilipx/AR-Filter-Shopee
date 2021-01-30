import 'dart:typed_data';
import 'dart:ui';

import 'package:firebase_shop_app/smile_painter.dart';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:firebase_ml_vision/firebase_ml_vision.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'dart:ui' as ui;
import 'package:image/image.dart' as image;
import 'utils.dart';

class FaceDetectionFromLiveCamera extends StatefulWidget {
  FaceDetectionFromLiveCamera({Key key}) : super(key: key);

  @override
  _FaceDetectionFromLiveCameraState createState() =>
      _FaceDetectionFromLiveCameraState();
}

class _FaceDetectionFromLiveCameraState
    extends State<FaceDetectionFromLiveCamera> {
  final FaceDetector faceDetector = FirebaseVision.instance.faceDetector();
  List<Face> faces;
  ui.Image limage;
  CameraController _camera;

  Future<ui.Image> getImage(String asset, int height, int width) async {
    ByteData data = await rootBundle.load(asset);
    image.Image baseSizeImage = image.decodeImage(data.buffer.asUint8List());
    image.Image resizeImage = image.copyResize(baseSizeImage, width: width);
    ui.Codec codec =
        await ui.instantiateImageCodec(image.encodePng(resizeImage));
    // Codec codec = await ui.instantiateImageCodec(data.buffer.asUint8List());
    FrameInfo fi = await codec.getNextFrame();
    return fi.image;
  }

  load(int height, int width) async {
    limage = await getImage('assets/images/sunglasses_2.png', height, width);
  }

  bool _isDetecting = false;
  CameraLensDirection _direction = CameraLensDirection.front;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  void _initializeCamera() async {
    CameraDescription description = await getCamera(_direction);
    ImageRotation rotation = rotationIntToImageRotation(
      description.sensorOrientation,
    );

    _camera = CameraController(
      description,
      defaultTargetPlatform == TargetPlatform.iOS
          ? ResolutionPreset.low
          : ResolutionPreset.medium,
    );
    await _camera.initialize();

    _camera.startImageStream((CameraImage image) {
      if (_isDetecting) return;

      _isDetecting = true;

      detect(image, FirebaseVision.instance.faceDetector().processImage,
              rotation)
          .then(
        (dynamic result) {
          setState(() {
            faces = result;
          });

          _isDetecting = false;
        },
      ).catchError(
        (_) {
          _isDetecting = false;
        },
      );
    });
  }

  Widget _buildResults() {
    const Text noResultsText = const Text('No results!');

    if (faces == null || _camera == null || !_camera.value.isInitialized) {
      return noResultsText;
    }

    CustomPainter painter;

    final Size imageSize = Size(
      _camera.value.previewSize.height,
      _camera.value.previewSize.width,
    );

    if (faces is! List<Face>) return noResultsText;
    for (var i = 0; i < faces.length; i++) {
      load(faces[i].boundingBox.height.floor(),
          (0.9 * faces[i].boundingBox.width).floor());
    }
    painter = SmilePainterLiveCamera(limage, imageSize, faces);

    return CustomPaint(
      painter: painter,
    );
  }

  Widget _buildImage() {
    return Container(
      constraints: const BoxConstraints.expand(),
      child: _camera == null
          ? const Center(
              child: Text(
                'Initializing Camera...',
                style: TextStyle(
                  color: Colors.green,
                  fontSize: 30.0,
                ),
              ),
            )
          : Stack(
              fit: StackFit.expand,
              children: <Widget>[
                CameraPreview(_camera),
                _buildResults(),
                Positioned(
                  bottom: 0.0,
                  left: 0.0,
                  right: 0.0,
                  child: Container(
                    color: Colors.white,
                    height: 50.0,
                    child: ListView(
                      children: faces
                          .map((face) =>
                              Text(face.boundingBox.center.toString()))
                          .toList(),
                    ),
                  ),
                ),
              ],
            ),
    );
  }

  void _toggleCameraDirection() async {
    if (_direction == CameraLensDirection.back) {
      _direction = CameraLensDirection.front;
    } else {
      _direction = CameraLensDirection.back;
    }

    await _camera.stopImageStream();
    await _camera.dispose();

    setState(() {
      _camera = null;
    });

    _initializeCamera();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Face Detection with Smile"),
      ),
      body: _buildImage(),
      floatingActionButton: FloatingActionButton(
        onPressed: _toggleCameraDirection,
        child: _direction == CameraLensDirection.back
            ? const Icon(Icons.camera_front)
            : const Icon(Icons.camera_rear),
      ),
    );
  }
}
