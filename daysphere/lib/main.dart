import 'package:flutter/material.dart';

void main() {
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
            seedColor: const Color.fromARGB(255, 34, 6, 138)),
        useMaterial3: true,
      ),
      home: Material(
        child: Row(
          children: [
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Calendar(
                  key: key,
                ),
              ),
            ),
            EventViewer(key: key),
          ],
        ),
      ),
    );
  }
}

class Calendar extends StatefulWidget {
  const Calendar({super.key});

  @override
  State<Calendar> createState() => _CalendarState();
}

class _CalendarState extends State<Calendar> {
  int nodeIndex = 0;

  int indexSetter() {
    if (nodeIndex > 30) {
      nodeIndex = 0;
    }
    nodeIndex += 1;
    return nodeIndex;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        const CalendarHeader(),
        Expanded(
          child: StaticGrid(
            columnCount: 7,
            columnMainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              CalendarNode(calendarIndex: 1, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 2, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 3, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 4, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 5, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 6, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 7, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 1, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 2, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 3, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 4, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 5, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 6, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 7, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 1, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 2, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 3, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 4, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 5, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 6, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 7, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 1, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 2, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 3, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 4, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 5, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 6, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 7, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 1, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 2, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 3, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 4, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 5, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 6, dayNumber: indexSetter()),
              CalendarNode(calendarIndex: 7, dayNumber: indexSetter()),
            ],
          ),
        ),
      ],
    );
  }
}

// Displays all the the Moday - Sunday above the nodes.
class CalendarHeader extends StatelessWidget {
  const CalendarHeader({super.key});

  @override
  Widget build(BuildContext context) {
    final style = Theme.of(context).textTheme.labelLarge!.copyWith(
          color: Colors.black,
        );
    return Padding(
      padding: const EdgeInsets.fromLTRB(0, 12, 0, 0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Text(
            'Monday',
            style: style,
          ),
          Text(
            'Tuesday',
            style: style,
          ),
          Text(
            'Wednesday',
            style: style,
          ),
          Text(
            'Thursday',
            style: style,
          ),
          Text(
            'Friday',
            style: style,
          ),
          Text(
            'Saturday',
            style: style,
          ),
          Text(
            'Sunday',
            style: style,
          ),
        ],
      ),
    );
  }
}

class CalendarNode extends StatefulWidget {
  final int calendarIndex;
  final int dayNumber;
  const CalendarNode({
    Key? key,
    required this.calendarIndex,
    required this.dayNumber,
  }) : super(key: key);

  @override
  State<CalendarNode> createState() => _CalendarNodeState();
}

class _CalendarNodeState extends State<CalendarNode> {
  String appointDayName() {
    switch (widget.calendarIndex % 7) {
      case 0:
        return 'Sunday';
      case 1:
        return 'Monday';
      case 2:
        return 'Tuesday';
      case 3:
        return 'Wednesday';
      case 4:
        return 'Thursday';
      case 5:
        return 'Friday';
      case 6:
        return 'Saturday';
    }
    return 'Sunday';
  }

  @override
  Widget build(BuildContext context) {
    final style = Theme.of(context).textTheme.titleLarge!.copyWith(
          color: Colors.black,
        );
    return Container(
      height: 100,
      width: 100,
      decoration: const BoxDecoration(
        border: Border(
          top: BorderSide(
            width: 1,
          ),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 8, 0, 0),
        child: Text(
          widget.dayNumber.toString(),
          style: style,
        ),
      ),
    );
  }
}

class StaticGrid extends StatelessWidget {
  const StaticGrid({
    Key? key,
    this.columnCount = 2,
    this.gap,
    this.padding,
    this.columnMainAxisAlignment = MainAxisAlignment.start,
    this.columnCrossAxisAlignment = CrossAxisAlignment.center,
    this.rowMainAxisAlignment = MainAxisAlignment.start,
    this.rowCrossAxisAlignment = CrossAxisAlignment.center,
    required this.children,
  }) : super(key: key);

  final int columnCount;
  final double? gap;
  final EdgeInsets? padding;
  final MainAxisAlignment columnMainAxisAlignment;
  final CrossAxisAlignment columnCrossAxisAlignment;
  final MainAxisAlignment rowMainAxisAlignment;
  final CrossAxisAlignment rowCrossAxisAlignment;
  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding,
      child: Column(
        crossAxisAlignment: columnCrossAxisAlignment,
        mainAxisAlignment: columnMainAxisAlignment,
        children: _createRows(),
      ),
    );
  }

  List<Widget> _createRows() {
    final List<Widget> rows = [];
    final childrenLength = children.length;
    final rowCount = (childrenLength / columnCount).ceil();

    for (int rowIndex = 0; rowIndex < rowCount; rowIndex++) {
      final List<Widget> columns = _createCells(rowIndex);
      rows.add(
        Row(
          crossAxisAlignment: rowCrossAxisAlignment,
          mainAxisAlignment: rowMainAxisAlignment,
          children: columns,
        ),
      );
      if (rowIndex != rowCount - 1) {
        rows.add(SizedBox(height: gap));
      }
    }

    return rows;
  }

  List<Widget> _createCells(int rowIndex) {
    final List<Widget> columns = [];
    final childrenLength = children.length;

    for (int columnIndex = 0; columnIndex < columnCount; columnIndex++) {
      final cellIndex = rowIndex * columnCount + columnIndex;
      if (cellIndex <= childrenLength - 1) {
        columns.add(Expanded(child: children[cellIndex]));
      } else {
        columns.add(Expanded(child: Container()));
      }

      if (columnIndex != columnCount - 1) {
        columns.add(SizedBox(width: gap));
      }
    }

    return columns;
  }
}

class EventViewer extends StatefulWidget {
  const EventViewer({super.key});

  @override
  State<EventViewer> createState() => _EventViewerState();
}

class _EventViewerState extends State<EventViewer> {
  @override
  Widget build(BuildContext context) {
    final style = Theme.of(context).textTheme.displaySmall!.copyWith(
          color: Colors.black,
        );
    final style2 = Theme.of(context).textTheme.titleLarge!.copyWith(
          color: Colors.black,
        );
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Container(
        width: 300,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          border: Border.all(width: 2),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 10, 0, 14),
              child: Text(
                '1',
                style: style,
              ),
            ),
            Container(
              height: 2,
              width: 300,
              color: Colors.black,
            ),
            Center(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(20, 20, 20, 0),
                child: Text(
                  'Nothing planned for the day!',
                  style: style2,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
