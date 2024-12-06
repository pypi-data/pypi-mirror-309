import click

from toutiao import version_info
from toutiao.core import TouTiao


CONTEXT_SETTINGS = dict(
    help_option_names=['-?', '-h', '--help'],
    max_content_width=200,
)

__epilog__ = click.style('''

\b
examples:
    {prog} -u xxxxx -t xxxxx
    {prog} -u xxxxx -t xxxxx -d output
    {prog} -u xxxxx -t xxxxx -l 5
    {prog} -u xxxxx -t xxxxx -l 1 -d 1080p
    {prog} -u xxxxx -t xxxxx -l 10 --dryrun
                              
\x1b[34mcontact: {author} <{author_email}>
''', fg='yellow').format(**version_info)

@click.command(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    epilog=__epilog__,
)
@click.option('-u', '--user-id', help='the user_id (token)', required=True)
@click.option('-t', '--tt-webid', help='the tt_webid in cookies', required=True, envvar='TT_WEBID', show_envvar=True)
@click.option('-O', '--outdir', help='output directory', default='download', show_default=True)
@click.option('-d', '--definition', help='the video definition to download', default='720p')
@click.option('-l', '--limit', help='the max number of videos to download', type=int, default=1, show_default=True)
@click.option('--dryrun', help='dryrun mode', is_flag=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
def cli(user_id, tt_webid, outdir, definition, limit, dryrun):

    toutiao = TouTiao(user_id=user_id, tt_webid=tt_webid)

    for n, item in enumerate(toutiao.list_user_feed(), 1):
        print(n, item['title'])

        if dryrun:
            toutiao.show_video_list(item, definition=definition)
        else:
            toutiao.download(item, definition=definition, outdir=outdir)

        if n >= limit:
            break


def main():
    cli()


if __name__ == '__main__':
    main()
