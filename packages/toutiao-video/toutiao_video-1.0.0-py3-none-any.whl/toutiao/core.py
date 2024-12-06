import os

import loguru
import human_readable
from webrequests import WebRequest as WR


class TouTiao(object):
    url = 'https://www.toutiao.com/api/pc/list/user/feed'

    def __init__(self, user_id, tt_webid=None):
        self.user_id = user_id
        self.cookies = {'tt_webid': tt_webid}

    def list_user_feed(self, max_behot_time=0, category='pc_profile_video'):
        params = {
            'token': self.user_id,
            'category': category,
            'max_behot_time': max_behot_time,
        }
        response = WR.get_response(self.url, params=params, cookies=self.cookies)
        try:
            data = response.json()
        except Exception as e:
            loguru.logger.error('response error, please check your input or `TT_WEBID`')
            exit(1)

        for item in data['data']:
            context = {
                'title': item['title'],
                'video_id': item['video_id'],
                'video_url': item['video']['download_addr']['url_list'][0],
                'video_list': self._get_video_list(item['video']['play_addr_list'])
            }
            yield context

        if data['has_more']:
            next_max_behot_time = data['next']['max_behot_time']
            yield from self.list_user_feed(max_behot_time=next_max_behot_time, category=category)

    def _get_video_list(self, play_addr_list):

        def get_context(play_addr_list):
            for item in play_addr_list:
                key = item['definition'].lower()
                value = {
                    'url': item['play_url_list'][0],
                    'size': item['size'],
                    'vtype': item['vtype'],
                }
                yield key, value
        
        return dict(get_context(play_addr_list))
    
    def download(self, context, definition='720p', outfile=None, outdir='download'):
        url = context['video_list'][definition]['url']
        outfile = outfile or context['title'] + '.mp4'
        if outdir:
            outfile = os.path.join(outdir, outfile)
        WR.download(url, outfile=outfile)

    def show_video_list(self, context, definition='all'):
        video_list = {definition: context['video_list'].get(definition)} if definition in context['video_list'] else context['video_list']
        for d in video_list:
            print('*' * 80)
            print('definition:', d)
            print('size:', human_readable.file_size(video_list[d]['size'], gnu=True))
            print('url:', video_list[d]['url'])
        print('*' * 80)


if __name__ == '__main__':
    user_id = 'MS4wLjABAAAAgNo1ltfFJDUq0t3oI9Xxs9R4L0F4VeShp-GTKwvK5ScLYhUvKfTp5r5gBH-rTSWB'
    tt_webid = '7404886214262621750'
    toutiao = TouTiao(user_id, tt_webid=tt_webid)
    items = toutiao.list_user_feed()
    for n, item in enumerate(items, 1):
        print(n, item['title'])

        # toutiao.download(item)
        toutiao.show_video_list(item, definition='1080p')

        if n >= 2:
            break