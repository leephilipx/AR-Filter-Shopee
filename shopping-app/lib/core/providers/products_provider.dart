import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:firebase_shop_app/core/providers/product_model_provider.dart';
import 'package:flutter/material.dart';

class ProductsProvider with ChangeNotifier {
  List<ProductModelProvider> _products = [
    ProductModelProvider(
      id: '7949086472',
      title: 'Protective Eye Goggles',
      description:
          'Protective Eye Goggles Safety Transparent Glasses Medical Use goggle Eyeglasses',
      price: 1.51,
      imageUrl: 'https://cf.shopee.sg/file/56823b835b801e7551559f8fb662589c',
    ),
    // ProductModelProvider(
    //     id: 'p2',
    //     title: 'Trousers',
    //     description: 'A nice pair of trousers.',
    //     price: 59.99,
    //     imageUrl:
    //         'https://i.shgcdn.com/6f18c86f-f2b7-4c90-a21d-0c3cd3ff8ade/-/format/auto/-/preview/3000x3000/-/quality/lighter/'),
    // ProductModelProvider(
    //   id: 'p3',
    //   title: 'Yellow Scarf',
    //   description: 'Warm and cozy - exactly what you need for the winter.',
    //   price: 19.99,
    //   imageUrl:
    //       'https://www.pngarts.com/files/3/Men-Jacket-Download-Transparent-PNG-Image.png',
    // ),
    // ProductModelProvider(
    //   id: 'p4',
    //   title: 'A Pan',
    //   description: 'Prepare any meal you want.',
    //   price: 49.99,
    //   imageUrl:
    //       'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Cast-Iron-Pan.jpg/1024px-Cast-Iron-Pan.jpg',
    // ),
    // ProductModelProvider(
    //     id: 'p5',
    //     title: 'A Pan',
    //     description: 'Prepare any meal you want.',
    //     price: 49.99,
    //     imageUrl:
    //         'https://webcomicms.net/sites/default/files/clipart/170435/clothes-png-transparent-images-170435-4237336.png'),
    // ProductModelProvider(
    //     id: 'p6',
    //     title: 'A Pan',
    //     description: 'Prepare any meal you want.',
    //     price: 49.99,
    //     imageUrl:
    //         'https://toppng.com/uploads/preview/1st-in-firefighter-bear-pocket-t-black-firefighter-what-teddy-bear-clothes-fits-most-115690366871syjjukhtr.png'),
    // // ProductModelProvider(
    // //     id: 'p7',
    // //     title: 'A Pan',
    // //     description: 'Prepare any meal you want.',
    // //     price: 49.99,
    // //     imageUrl:
    // //         'http://s20.favim.com/orig/2018/08/09/png-short-png-clothes-png-112664-Favim.com.jpg'),
    // // ProductModelProvider(
    // //   id: 'p8',
    // //   title: 'A Pan',
    // //   description: 'Prepare any meal you want.',
    // //   price: 49.99,
    // //   imageUrl:
    // //       'https://img.favpng.com/15/5/21/1950s-dress-halterneck-clothing-polka-dot-png-favpng-CVsvfuuL83smqtH6b23jFVrLz.jpg',
    // // ),
  ];

  // getter
  //  List<Product> get products => [..._products];
  List<ProductModelProvider> get products {
    return _products;
  }

  List<ProductModelProvider> get favoriteProducts {
    return _products.where((product) => product.isFavorite).toList();
  }

  Future<void> addProduct(ProductModelProvider product) {
    const String url =
        "https://flutter-shop-7ddca.firebaseio.com/products.json";
    return http
        .post(url,
            body: json.encode({
              'title': product.title,
              'description': product.description,
              'imageUrl': product.imageUrl,
              'price': product.price,
              'isFavorite': product.isFavorite,
            }))
        .then((response) {
      _products.add(product);
      notifyListeners();
    }).catchError((err) {
      // Print Something ...
    });
  }

  void getAllProducts() {
    _products = [];
    getProduct("7949086472", "299085382");
    getProduct("1123430218", "16175315");
    getProduct("3631790694", "35589275");
  }

  Future<void> getProduct(String itemid, String shopid) {
    String url = "https://api.hackathon2021.shopee.sg/item/get_info?item_id=" +
        itemid +
        "&shop_id=" +
        shopid;
    return http.get(
      url,
      headers: {"X-Hackathon-Token": "BkdJmJtUKWGzZYryYaUX"},
    ).then((response) {
      // print(response.body);
      var body = response.body;
      final parsed = jsonDecode(body);
      print(parsed);
      var length = _products.length;
      print(length);
      var newProduct = ProductModelProvider(
        id: "p$length",
        title: (parsed['data']['name']),
        description: parsed['data']['name'],
        // price: double.parse(parsed['data']['price']),
        price: parsed['data']['price'],
        imageUrl: parsed['data']['cover'],
      );
      _products.add(newProduct);
      notifyListeners();
    }).catchError((err) {
      // Print Something ...
    });
  }

  void updateProduct(String id, ProductModelProvider product) {
    final productIndex = _products.indexWhere((prod) => prod.id == id);
    if (productIndex >= 0) {
      _products[productIndex] = product;
      notifyListeners();
    }
  }

  void deleteProduct(String id) {
    _products.removeWhere((prod) => prod.id == id);
    notifyListeners();
  }

  ProductModelProvider findProductById(String id) {
    return _products.firstWhere((product) => product.id == id);
  }

  void addProductToFavourite(String id) {
    final product = _products.firstWhere((product) => product.id == id);
    if (product.isFavorite == false) {
      product.isFavorite = true;
      notifyListeners();
    }
  }

  void removeProductFromFavourite(String id) {
    final product = _products.firstWhere((product) => product.id == id);
    if (product.isFavorite) {
      product.isFavorite = false;
      notifyListeners();
    }
  }
}
