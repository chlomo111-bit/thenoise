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
    pg.goto('http://local/index.html?demo');pg.wait_for_timeout(2500);pg.click('#enter');pg.wait_for_timeout(5000)
    pg.fill('#q','user_3');pg.click('#sf button');pg.wait_for_timeout(1500);pg.screenshot(path='/tmp/r_card.png');pg.evaluate("document.getElementById('claim')&&document.getElementById('claim').click()")
    for i in range(4):pg.click('#bClap');pg.wait_for_timeout(250)
    pg.click('#bTom');pg.wait_for_timeout(350);pg.screenshot(path='/tmp/r_fly.png');pg.wait_for_timeout(900);pg.screenshot(path='/tmp/r_splat.png')
    pg.click('text=השורה הראשונה');pg.wait_for_timeout(400);pg.screenshot(path='/tmp/r_vip.png')
    b.close()
