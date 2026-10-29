import sys,os
from playwright.sync_api import sync_playwright
root='/home/claude/thenoise'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for vp,name in [({'width':390,'height':844},'mobile'),({'width':1280,'height':800},'desk')]:
        pg=b.new_page(viewport=vp)
        pg.on('pageerror',lambda e:print('ERR',e));pg.on('console',lambda m:print('console',m.text) if m.type=='error' else None)
        pg.route('**/three.min.js',lambda r:r.fulfill(path='/root/noise/three.min.js'))
        pg.route('**/OrbitControls.js',lambda r:r.fulfill(path='/root/noise/node_modules/three/examples/js/controls/OrbitControls.js'))
        pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(body='',content_type='text/css'))
        pg.route('http://local/**',lambda r:r.fulfill(path=root+'/'+r.request.url.split('http://local/')[1].split('?')[0]))
        pg.goto('http://local/index.html?demo');pg.wait_for_timeout(2500)
        pg.screenshot(path=f'/tmp/site_{name}_intro.png')
        pg.click('#enter');pg.wait_for_timeout(3500);pg.screenshot(path=f'/tmp/site_{name}_stage.png')
        pg.click('text=המתמודדים');pg.wait_for_timeout(500);pg.screenshot(path=f'/tmp/site_{name}_cont.png')
        pg.click('#p-cont .x');pg.fill('#q','@user_5');pg.click('#sf button');pg.wait_for_timeout(2500);pg.screenshot(path=f'/tmp/site_{name}_find.png')
        pg.close()
    b.close()
