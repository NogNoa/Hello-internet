"""
a simple script to log in to facebook.com and post a silly post
"""

from selenium import webdriver
id = open('id.txt', 'r').readlines()


class FaceBot():
    def __init__(self):
        self.driver = webdriver.Firefox()
    def wndw_swtch(self,n):
        'switch to another window'
        windows: list = self.driver.window_handles
        self.driver.switch_to.window(windows[n])
    def login(self):
        self.driver.get('https://www.facebook.com')
        def el_in(x,n):
            element=self.driver.find_element_by_xpath(x)
            element.send_keys(id[n])
        el_in('//*[@id="email"]',0)
        el_in('//*[@id="pass"]',1)
        def press():
            try:
                log_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/table/tbody/tr[2]/td[3]')
            except:
                log_button = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/form/div[2]/button')
            print(type(log_button))
            log_button.click()
        press()
    def post(self,msg):
        mood = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div/div/div')
        #//*[@id="pagelet_composer"]
        #/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div
        mood.click()
        mood = self.driver.find_element_by_partial_link_text('<div data-contents="true"><div class="" data-block="true" data-editor="nmle" data-offset-key="e6vso-0-0"><div data-offset-key="e6vso-0-0" class="_1mf _1mj"><span data-offset-key="e6vso-0-0"><br data-text="true"></span></div></div></div>')
        #'html#facebook body.hasLeftCol._2yq.home.composerExpanded._5vb_.fbx._-kb._605a.b_1k_okfhg1_.gecko.x1-5.Locale_en_GB.cores-gte4._19_u.hasAXNavMenubar div#u_0_o._li div#globalContainer.uiContextualLayerParent div#content.fb_content.clearfix div div#mainContainer.clearfix._2pie div#contentCol._5r-_.homeWiderContent.homeFixedLayout.newsFeedComposer._1qkq._1ql0 div#content_container.clearfix div#contentArea._14i5._1qkq._1qkx div#stream_pagelet div#pagelet_composer div div._3u13._3e9r._3u14._1b3n div._3u16 div div#feedx_sprouts_container._nh6._3qd3 div._1cx1._4a8c._4aay._4ab3 div#rc.u_0_14._5n2b._36bx._4-u2._4-u8 div._4zoz._5xv3._4cw._4-u3 div#js_12 div._i-o._2j7c div._3eny div._7r84 div.clearfix._ikh div._4bl9 div div div._3nd0 div._1mwp.navigationFocus._395._1mwq._4c_p._5bu_._3t-3._34nd._21mu._5yk1 div._5yk2 div._5rp7 div._5rpb div.notranslate._5rpu')
        #/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div')
        #/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div
        #/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div
        mood.send_keys(msg)

face=FaceBot()
face.login()
face.post('Hello Internet')







