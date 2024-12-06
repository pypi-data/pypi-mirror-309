#!/usr/bin/env python3
import click 
@click.command()
@click.option('--port','-p',default=8080,help='端口设置')
@click.option('--ssl',default=False,help="采用ssl加密",is_flag=True)
@click.option('--ipv6',default=False,help="采用ipv6加密",is_flag=True)
@click.option('--check_login',default=False,help="是否检查用户登录",is_flag=True)
@click.option('--flask',default=False,help="采用flask框架，默认是web.py框架",is_flag=True)
@click.option('--poster',default=False,help="自动生成缩略图",is_flag=True)
@click.option('--icon',default=False,help="使用icon图标",is_flag=True)
def main(port,ssl,flask,ipv6,check_login,poster,icon):
    if not flask:
        from . import web_server as server
    else:
        from . import flask_server as server
    server.main(port,ssl,ipv6=ipv6,check_user=check_login,generate_poster=poster,icon=icon)
if __name__=='__main__':
    main()