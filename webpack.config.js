module.exports = {
  entry: ["./app.js"],
  mode:"development",  //
  //mode:"production",  //
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {}
          }
        ]
      },
			{
        test: /\.(glsl|vs|fs)$/,
        loader: 'shader-loader',
        options: {
          glsl: {
            //chunkPath: resolve("/src/")
          }
        }
      }
    ]
  }, 
  devServer: {
          host: '0.0.0.0',
          port: 8080
  },
  output: {
    filename: "bundle.js",
    //publicPath: "/assets/"
  }, 
  watch: true
}


