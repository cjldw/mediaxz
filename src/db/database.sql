-- 微博
-- 视频表
create table videos
(
  id           integer primary key autoincrement,
  code         TEXT                default '' unique,
  url          TEXT                default '',
  img          TEXT                default '',
  title        TEXT                default '',
  href         TEXT                default '',
  created_date text                default current_timestamp
);

-- 花瓣
-- 图片表
create table images (
  id           integer primary key autoincrement,
  hash         text                default '' unique,
  url          text                default '',
  width        integer             default '0',
  height       integer             default '0',
  created_date text                default current_timestamp
);

-- 图片记录边界表
create table image_record_index (
  id           integer primary key autoincrement,
  record_index integer             default '0',
  created_date text                default current_timestamp
);

-- 视频数据

create table videos_stream (
  id           integer primary key autoincrement,
  code         text                default '' unique,
  url          text                default '',
  title        text                default '',
  created_date text                default current_timestamp
);

create table videos_stream_index (
  id           integer primary key autoincrement,
  record_index integer             default '0',
  created_date text                default current_timestamp
);