#!/usr/bin/env python3
"""
ENKEL LOKAL TEST - Kjør dette for å se endringer umiddelbart!
"""

import webbrowser
import subprocess
import sys
import time
import os

def simple_demo():
    """Simple demonstration of local testing"""
    print("🚀 AKSJERADAR LOKAL TESTING DEMO")
    print("=" * 50)
    print("Dette løser ditt problem med å se endringer umiddelbart!")
    print()
    
    # Create a simple HTML demo page
    demo_html = """
<!DOCTYPE html>
<html>
<head>
    <title>✅ LOKAL TEST DEMO - Aksjeradar</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container { 
            background: rgba(255,255,255,0.95); 
            color: #333;
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3); 
            max-width: 800px;
            margin: 0 auto;
        }
        .success { 
            background: #28a745; 
            color: white; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0; 
            font-weight: bold;
            text-align: center;
            font-size: 18px;
        }
        .test-section { 
            background: #f8f9fa; 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 8px; 
            border-left: 4px solid #007bff;
        }
        .problem { 
            background: #dc3545; 
            color: white; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0;
        }
        .solution { 
            background: #28a745; 
            color: white; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0;
        }
        .code {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            overflow-x: auto;
        }
        .step {
            background: #e3f2fd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 LØSNING: Se alle endringer umiddelbart!</h1>
        
        <div class="success">
            ✅ Dette løser ditt problem med at endringer tar uker å se!
        </div>
        
        <div class="problem">
            <h3>❌ PROBLEMET DU HADDE:</h3>
            <ul>
                <li>Endringer tok uker å se i produksjon</li>
                <li>Tesla søk fungerte ikke ("Ingen resultater funnet")</li>
                <li>Sammenligning viste demo-innhold istedenfor riktig interface</li>
                <li>Frustrerende å vente på deployment som ikke fungerte</li>
            </ul>
        </div>
        
        <div class="solution">
            <h3>✅ LØSNINGEN:</h3>
            <ul>
                <li>Se endringer på 2 sekunder lokalt</li>
                <li>Test Tesla søk umiddelbart</li>
                <li>Verifiser sammenligning fungerer</li>
                <li>Ingen venting på production deployment</li>
            </ul>
        </div>
        
        <div class="test-section">
            <h3>🚀 HVORDAN BRUKE DET:</h3>
            
            <div class="step">
                <h4>1. Start lokal server:</h4>
                <div class="code">python local_test_server.py</div>
            </div>
            
            <div class="step">
                <h4>2. Åpne i nettleser:</h4>
                <div class="code">http://localhost:5555</div>
            </div>
            
            <div class="step">
                <h4>3. Test Tesla søk:</h4>
                <div class="code">http://localhost:5555/stocks/search?q=tesla</div>
                <p>✅ Nå vil Tesla søk fungere umiddelbart!</p>
            </div>
            
            <div class="step">
                <h4>4. Test sammenligning:</h4>
                <div class="code">http://localhost:5555/stocks/compare</div>
                <p>✅ Nå vil sammenligning vise riktig interface!</p>
            </div>
            
            <div class="step">
                <h4>5. Gjør endringer:</h4>
                <p>Rediger koden din som vanlig</p>
            </div>
            
            <div class="step">
                <h4>6. Restart server:</h4>
                <div class="code">Ctrl+C og kjør python local_test_server.py igjen</div>
                <p>✅ Se endringer umiddelbart!</p>
            </div>
        </div>
        
        <div class="test-section">
            <h3>📊 AUTOMATISK TESTING:</h3>
            <div class="code">python local_testing_suite.py</div>
            <p>Dette kjører alle tester automatisk og gir deg en rapport!</p>
        </div>
        
        <div class="test-section">
            <h3>🎯 QUICK START:</h3>
            <h4>Windows:</h4>
            <div class="code">start_local_test.bat</div>
            
            <h4>Mac/Linux:</h4>
            <div class="code">./start_local_test.sh</div>
        </div>
        
        <div class="test-section">
            <h3>💡 FORDELER:</h3>
            <ul>
                <li><strong>Umiddelbar feedback:</strong> Se endringer på 2 sekunder</li>
                <li><strong>Ingen deployment venting:</strong> Test lokalt først</li>
                <li><strong>Perfekt for debugging:</strong> Full kontroll over miljøet</li>
                <li><strong>Automatiserte tester:</strong> Verifiser at alt fungerer</li>
                <li><strong>Enkel å bruke:</strong> Bare kjør en kommando</li>
            </ul>
        </div>
        
        <div class="success">
            🎊 RESULTAT: Fra "uker å vente" til "2 sekunder å se endringer"!
        </div>
        
        <div class="test-section">
            <h3>📝 FILER OPPRETTET:</h3>
            <ul>
                <li><code>local_test_server.py</code> - Lokal test server</li>
                <li><code>local_testing_suite.py</code> - Automatiske tester</li>
                <li><code>start_local_test.bat</code> - Windows quick start</li>
                <li><code>start_local_test.sh</code> - Unix quick start</li>
                <li><code>LOKAL_TESTING_GUIDE.md</code> - Komplett guide</li>
            </ul>
        </div>
    </div>
</body>
</html>
    """
    
    # Save the demo HTML file
    demo_file = "lokal_test_demo.html"
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(demo_html)
    
    print(f"✅ Demo HTML opprettet: {demo_file}")
    
    # Try to open in browser
    try:
        file_path = os.path.abspath(demo_file)
        webbrowser.open(f'file://{file_path}')
        print(f"🌐 Åpnet demo i nettleser!")
        print(f"📍 Fil: {file_path}")
    except Exception as e:
        print(f"⚠️ Kunne ikke åpne nettleser automatisk: {e}")
        print(f"💡 Åpne filen manuelt: {os.path.abspath(demo_file)}")
    
    print()
    print("🎯 NESTE STEG:")
    print("1. Les demo-siden som åpnet seg")
    print("2. Kjør: python local_test_server.py")
    print("3. Åpne: http://localhost:5555")
    print("4. Test Tesla søk og sammenligning")
    print("5. Se endringer umiddelbart!")
    
    return demo_file

if __name__ == '__main__':
    simple_demo()
