import 'package:flutter/material.dart';
import "package:satis_planner/testmod.dart";
import "package:python_ffi/python_ffi.dart";

void pythontest(arg) async {
  WidgetsFlutterBinding.ensureInitialized();
  await PythonFfi.instance.initialize();
  print(TestModule.import().testfunc(arg));
}
void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
          floatingActionButton: FloatingActionButton(
            onPressed: () {
              pythontest("You");
              // Onpress Code
            },
            child: const Icon(Icons.mic),
          ),
          appBar: const Tab(
            child: Text("data"),
          ),
          body: const DraggableItem()),
    );
  }
}

class DraggableItem extends StatefulWidget {
  const DraggableItem({
    super.key,
    // this.child
  });

  @override
  State<DraggableItem> createState() => _DraggableItemState();
}

class _DraggableItemState extends State<DraggableItem> {
  double _left = 0;
  double _top = 0;

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Positioned(
          left: _left,
          top: _top,
          child: GestureDetector(
            onPanUpdate: (details) {
              setState(() {
                _left += details.delta.dx;
                _top += details.delta.dy;
              });
            },
            child: Container(
              color: Colors.black,
              child: Image.asset(
                'images/constructor.png',
                width: 100,
                height: 100,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
