#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
    @File: main.py
    @Create: 2020/7/12 16:45
    @Version: V1.0-base
    @Author: afeng
    @Contact: afeng616@gmail.com
    @Description: 
"""
from operate.evaluate import Evaluate
import os

if __name__ == '__main__':
    print("""
        ___    ___         _ _ _ _         ||         _ _ _ _    
      /     \/     \     /  9_9_9  \      (  )      / n  .  n \  
     |   m      m   |   |  @     @  |    (____)    |    / \    | 
     |  |  |  |  |  |   |  V  *  V  |      ii      |   |   |   | 
     |  |   oo   |  |   |  V  ^  V   \     ii      |   |   |   | 
     |__|        |__|    \_V_ _ _V/\__\    ii      |_ _|   |_ _| 
    """)
    Evaluate(os.path.dirname(__file__)).evaluate()
