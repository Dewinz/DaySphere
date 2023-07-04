import "package:python_ffi/python_ffi.dart";

final class BasicCliAdder extends PythonModule {
  BasicCliAdder.from(super.pythonModule) : super.from();

  static BasicCliAdder import() =>
      PythonFfi.instance.importModule("basic_cli_adder", BasicCliAdder.from);

  num add(num x, num y) => getFunction("add").call(<Object?>[x, y]);
}
