import "package:python_ffi/python_ffi.dart";

final class TestModule extends PythonModule {
  TestModule.from(super.pythonModule) : super.from();

  static TestModule import() =>
    PythonFfi.instance
      .importModule("testmod", TestModule.from);

  String testfunc(String arg) => getFunction("testfunc").call(<Object?>[arg]);
}