import "package:satis_planner/testmod.dart";
import "package:flutter/material.dart";
import "package:python_ffi/python_ffi.dart";

void main(List<String> arguments) async {
  final String arg = arguments[0];

  WidgetsFlutterBinding.ensureInitialized();
  await PythonFfi.instance.initialize();

  final TestModule testModule = TestModule.import();
  final String result = testModule.testfunc(arg);
  print("$arg = $result");
}