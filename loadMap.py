from  wolfenscii  import wap

if __name__ == "__main__":
    
    res =   wap.readMap('wolfenscii/asset/map/map1.uxf')
    print res
    rootNode = wap.buildRootNode(res)



