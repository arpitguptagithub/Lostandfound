import 'dart:html';
import 'dart:js_util';

import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MyAppState(),
      child: MaterialApp(
        title: 'Namer App',
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        ),
        home: MyHomePage(),
      ),
    );
  }
}

class MyAppState extends ChangeNotifier {
  var current = WordPair.random();

  void getNext() {
    current = WordPair.random();
    notifyListeners();
  }

  var favorites = <WordPair>[];

  void toggleFavorite() {
    if (favorites.contains(current)) {
      favorites.remove(current);
    } else {
      favorites.add(current);
    }
    notifyListeners();
  }
}

class MyHomePage extends StatefulWidget {
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    Widget page;
    switch (selectedIndex) {
      case 0:
        page = GeneratorPage();
        break;
      case 1:
        // page = Home_screen_culturia();
        page = Home_screen_culturia();
        break;
      default:
        throw UnimplementedError('no widget for $selectedIndex');
    }

    return Scaffold(
      body: Row(
        children: [
          SafeArea(
            child: NavigationRail(
              extended: false,
              destinations: [
                const NavigationRailDestination(
                  icon: Icon(Icons.home),
                  label: Text('Home'),
                ),
                const NavigationRailDestination(
                  icon: Icon(Icons.favorite),
                  label: Text('Favorites'),
                ),
              ],
              selectedIndex: selectedIndex,
              onDestinationSelected: (value) {
                setState(() {
                  selectedIndex = value;
                });
              },
            ),
          ),
          Expanded(
            child: Container(
              color: Theme.of(context).colorScheme.primaryContainer,
              child: page,
            ),
          ),
        ],
      ),
    );
  }
}


class Home_screen_culturia extends StatelessWidget{
  @override 
  Widget build(BuildContext context){



    return Scaffold(
     backgroundColor: Colors.grey,
     appBar: AppBar(
          backgroundColor: Colors.white,
          elevation: 0,
          leading: IconButton(
            icon: Icon(Icons.menu,color: Colors.black,),
            onPressed: () {},

           ) ,
          ),

      body: SafeArea(
        child:Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Container(
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.white,
              ),
              padding: EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children:<Widget> [
                  Text("Chandra and nandha gay", style: TextStyle(color: Colors.black87 , fontSize:25 ),),
                  SizedBox(
                    height: 5,
                  ),
                   Text("SEX SEX SEX", style: TextStyle(color: Colors.black87 , fontSize:40 ),),
                   SizedBox(
                    height: 20,
                   ),
                   Container(
                    padding: EdgeInsets.all(5),
                    decoration: BoxDecoration(
                      color: Colors.grey,
                      borderRadius: BorderRadius.circular(15)
                    ),
                    child: TextField(
                      decoration: InputDecoration(
                        border: InputBorder.none,
                        prefixIcon: Icon(Icons.search, color: Colors.black87,),
                        hintText: "GAy  IS MAANNU",
                        hintStyle: TextStyle(color: Colors.pink, fontSize: 20 )
                      ),
                    ),
                   ),
                   SizedBox(
                      height: 15,
                    ),  
                ],
              ),
            ),
            SizedBox( height: 20,),

            Padding(padding: const EdgeInsets.symmetric(horizontal: 30.0),
             child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Text("Bhenchod",
                style: TextStyle(fontStyle: FontStyle.italic ,fontSize: 13 ),
                ),
               SizedBox(
                height: 15,
              ),
               Container(
                      height: 200,
                      child: ListView(
                        scrollDirection: Axis.horizontal,
                        children: <Widget>[
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                          promoCard('assets/images/image.jpg'),
                           // need to work to make promocard popup
                        ],
                      ),
                    ),

                    SizedBox(
                      height: 20,
                    ),
                 
                  

              ],
             
             )
            
            
            
            
            ),


          ],
        
        
        
        
        ) 
      
      
      
      ),
);
  }
   
   Widget promoCard(image){
    return AspectRatio(aspectRatio: 2.8/3,
    child: Container(
      margin: EdgeInsets.only(right: 15.0),
      decoration: BoxDecoration(
     
        color: Colors.orange,
        borderRadius: BorderRadius.circular(10),
        image:DecorationImage(
          fit:BoxFit.cover
          ,image: AssetImage('assets/images/image.jpg')),
      ),
         child: Container(
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
              gradient: LinearGradient(begin: Alignment.bottomRight, stops:
               [ 0.1, 0.9 ],
                colors: [
                Colors.black.withOpacity(.8),
                Colors.black.withOpacity(.1)
              ])),
       
     ),
    ),
    );

   }
 
  }




class GeneratorPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    var pair = appState.current;

    IconData icon;
    if (appState.favorites.contains(pair)) {
      icon = Icons.favorite;
    } else {
      icon = Icons.favorite_border;
    }

    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          BigCard(pair: pair),
          const SizedBox(height: 10),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              ElevatedButton.icon(
                onPressed: () {
                  appState.toggleFavorite();
                },
                icon: Icon(icon),
                label: const Text('Like'),
              ),
              const SizedBox(width: 10),
              ElevatedButton(
                onPressed: () {
                  appState.getNext();
                },
                child: const Text('Next'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class BigCard extends StatelessWidget {
  const BigCard({
    super.key,
    required this.pair,
  });

  final WordPair pair;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final style = theme.textTheme.displayMedium!.copyWith(
      color: theme.colorScheme.onPrimary,
    );

    return Card(
      color: theme.colorScheme.primary,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Text(
          pair.asLowerCase,
          style: style,
          semanticsLabel: "${pair.first} ${pair.second}",
        ),
      ),
    );
  }
}
