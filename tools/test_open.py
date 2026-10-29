from playwright.sync_api import sync_playwright
root='/home/claude/thenoise'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':390,'height':844})
    pg.on('pageerror',lambda e:print('ERR',e))
    pg.route('**/three.min.js',lambda r:r.fulfill(path='/root/noise/three.min.js'))
    pg.route('**/OrbitControls.js',lambda r:r.fulfill(path='/root/noise/node_modules/three/examples/js/controls/OrbitControls.js'))
    pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(body='',content_type='text/css'))
    pg.route('http://local/**',lambda r:r.fulfill(path=root+'/'+r.request.url.split('http://local/')[1].split('?')[0]))
    pg.goto('http://local/index.html?demo');pg.wait_for_timeout(2500)
    pg.click('#enter')
    for i,w in enumerate([500,900,600,1500]):
        pg.wait_for_timeout(w);pg.screenshot(path=f'/tmp/open_{i}.png')
    print(pg.evaluate('AC?AC.state:"noaudio"'))
    b.close()
