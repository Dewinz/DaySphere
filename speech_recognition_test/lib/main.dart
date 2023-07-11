import 'package:flutter/material.dart';
import 'package:python_ffi/python_ffi.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await PythonFfi.instance.initialize();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Speech Recognition Test',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: const Color.fromARGB(255, 85, 58, 183)),
        useMaterial3: true,
      ),
      home: Material(
        child: RecorderWidget(
          key: key,
        ),
      ),
    );
  }
}

class RecorderWidget extends StatefulWidget {
  const RecorderWidget({
    super.key,
  });

  @override
  State<RecorderWidget> createState() => _RecorderWidgetState();
}

class _RecorderWidgetState extends State<RecorderWidget> {
  bool _isActivated = false;
  Color color = Colors.red;

  void _toggleActivation() {
    setState(() {
      if (_isActivated) {
        color = Colors.red;
        _isActivated = false;
      } else {
        color = Colors.green;
        _isActivated = true;
        // Here the python function should be called. IDK if a setstate is needed for the return.
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(
          height: 60,
        ),
        Row(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Container(
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10), color: color),
              height: 20,
              width: 20,
            ),
            const SizedBox(
              width: 40,
            ),
            ElevatedButton(
              onPressed: _toggleActivation,
              child: const Icon(Icons.mic),
            )
          ],
        ),
        const SizedBox(
          height: 40,
        ),
        const Text(
          "Balls in the walls.",
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
        )
      ],
    );
  }
}
