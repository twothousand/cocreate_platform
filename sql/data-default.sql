-- 插入测试数据 时间：2023-07-17
-- dim_ai_tags
INSERT INTO `dim_ai_tags` (id, ai_tag, created_at, updated_at, is_deleted)
VALUES
  (1, 'AI教育', '2023-07-17 14:32:08.900601000', '2023-07-17 14:32:08.900676000', 0),
  (2, 'AI绘画', '2023-07-17 14:32:13.667446000', '2023-07-17 14:32:13.667520000', 0),
  (3, 'AI写作', '2023-07-17 14:47:36.640970000', '2023-07-17 14:47:36.641065000', 0),
  (4, 'AI办公', '2023-07-17 14:47:56.075705000', '2023-07-17 14:47:56.075812000', 0),
  (5, 'AI视频', '2023-07-17 14:48:06.224635000', '2023-07-17 14:48:06.224805000', 0),
  (6, 'AI语音', '2023-07-17 14:48:11.996570000', '2023-07-17 14:48:11.996672000', 0),
  (7, 'AI图像', '2023-07-17 14:48:26.004937000', '2023-07-17 14:48:26.004978000', 0),
  (8, 'AI医疗', '2023-07-17 14:49:00.736098000', '2023-07-17 16:12:18.924040000', 0),
  (9, 'AI游戏', '2023-07-17 14:49:50.263937000', '2023-07-17 16:12:11.169088000', 0),
  (10, 'AI翻译', '2023-07-17 14:49:58.635972000', '2023-07-17 16:11:28.692371000', 0),
  (11, 'AI金融', '2023-07-17 14:50:16.366522000', '2023-07-17 14:50:16.366670000', 0),
  (12, 'AI法律', '2023-07-17 14:50:20.311391000', '2023-07-17 14:50:20.311500000', 0),
  (13, 'AI数字人', '2023-07-17 14:50:41.962546000', '2023-07-17 14:50:41.962632000', 0),
  (14, 'AI其它', '2023-07-17 14:50:48.886520000', '2023-07-17 14:50:48.886627000', 0);

-- dim_industry
INSERT INTO `dim_industry` (id, industry, created_at, updated_at, is_deleted)
VALUES
  (1, '教育', '2023-07-17 14:31:57.960313000', '2023-07-17 14:31:57.960378000', 0),
  (2, '医疗', '2023-07-17 14:32:02.062589000', '2023-07-17 14:32:02.062708000', 0),
  (3, '内容创作', '2023-07-17 14:56:57.548094000', '2023-07-17 14:56:57.548187000', 0),
  (4, '数据科学', '2023-07-17 14:57:41.277388000', '2023-07-17 14:57:41.277441000', 0),
  (5, '计算机', '2023-07-17 14:57:49.631830000', '2023-07-17 14:57:49.631906000', 0),
  (6, '金融', '2023-07-17 14:58:01.317150000', '2023-07-17 14:58:01.317290000', 0),
  (7, '零售', '2023-07-17 14:58:03.886155000', '2023-07-17 14:58:03.886294000', 0),
  (8, '农业', '2023-07-17 14:58:44.247488000', '2023-07-17 14:58:44.247620000', 0),
  (9, '制造业', '2023-07-17 14:58:46.902113000', '2023-07-17 14:58:46.902228000', 0),
  (10, '服务业', '2023-07-17 14:58:49.691714000', '2023-07-17 14:58:49.691822000', 0),
  (11, '健康', '2023-07-17 14:59:11.377039000', '2023-07-17 14:59:11.377099000', 0),
  (12, '汽车', '2023-07-17 14:59:27.552461000', '2023-07-17 14:59:27.552577000', 0),
  (13, '游戏', '2023-07-17 14:59:29.701562000', '2023-07-17 14:59:29.701596000', 0),
  (14, '其它', '2023-07-17 15:34:14.097149000', '2023-07-17 15:34:14.097238000', 0);

-- dim_model
INSERT INTO `dim_model` (id, model_name, model_type, model_source, model_description, is_open_source, created_at, updated_at, is_deleted)
VALUES
  (1, 'GPT-3.5', 'LLM', 'OpenAI', 'OpenAI大模型', 0, '2023-07-17 14:31:50.794586000', '2023-07-17 15:19:31.550502000', 0),
  (2, 'GPT-4', 'LLM', 'OpenAI', 'OpenAI最新的大语言模型', 0, '2023-07-17 15:16:05.292728000', '2023-07-17 15:16:05.292820000', 0),
  (3, 'Stable Diffusion', '扩散模型', 'Stability AI', '图像领域Diffusion扩散模型', 1, '2023-07-17 15:19:22.197755000', '2023-07-17 15:19:22.197832000', 0),
  (4, '文心大模型', 'LLM', '百度', '百度文心大模型', 0, '2023-07-17 15:21:35.967707000', '2023-07-17 15:21:35.967852000', 0),
  (5, '通义大模型', 'LLM', '阿里巴巴', '阿里：通义大模型', 0, '2023-07-17 15:22:22.451567000', '2023-07-17 15:22:22.451643000', 0),
  (6, '星火大模型', 'LLM', '讯飞', '讯飞：星火大模型', 0, '2023-07-17 15:23:17.985974000', '2023-07-17 15:23:17.986198000', 0),
  (7, 'ChatGLM2-6B', 'LLM', 'THUDM', '开源双语对话语言模型', 0, '2023-07-17 15:28:11.290235000', '2023-07-17 15:28:11.290300000', 0),
  (8, '其它', '其它', '其它', '其它', 0, '2023-07-17 15:29:53.547488000', '2023-07-17 15:29:53.547604000', 0);
  
-- message_template 消息模版
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.137578', 0, '01904ad9d6b8464d80e11f8962e72ab0', 'team_member_removal', '你已被抱出项目 {project_name}');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.116634', 0, '4ea3fa63c6df41f4bb4779caa9dcc5a8', 'product_reply', '{sender_nickname}回复了你的评论');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.106662', 0, '5bfdf28d52414acbb9dcb8a56f35bb9a', 'product_favorite', '{sender_nickname}收藏了你的产品{product_name}');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.111680', 0, '83e51cd76cf14bbf8801511b974ddb8e', 'product_comment', '{sender_nickname}评论了你的产品');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.121621', 0, 'a40a0cb6851540b88c9ba7e205fbae6b', 'team_application', '{sender_nickname}申请加入你的队伍 {project_name}');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.126608', 0, 'c346c84f3ec6489e8a5848b7000afc91', 'team_audit_result', '你的申请已通过，欢迎加入 {project_name}');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.132614', 0, 'e0c2a4f76ebd42d6bbc77cee21c0b5d4', 'team_leader_transfer', '你已成为{project_name} 项目的队长');
INSERT INTO `message_template`(`created_at`, `is_deleted`, `id`, `message_type`, `message_template`) VALUES ('2023-08-07 15:53:26.101676', 0, 'f7395bcd530b4b7aa212d70e2df398ca', 'product_like', '{sender_nickname}赞了你的产品{product_name}');

-- image 默认头像（要更改确认后的）
INSERT INTO `image` (`created_at`, `is_deleted`, `id`, `image_url`, `image_path`, `category`, `upload_user`, `updated_at`) VALUES ('2023-08-12 14:23:44.291232', 0, '61766174-6172-2d64-6566-61756c74fd67', 'https://cocreate-platform.oss-cn-hangzhou.aliyuncs.com/avatar/1691821423418_a1b9a3.png', 'avatar/1691821423418_a1b9a3.png', 'avatar', '1fe68988-6d71-4f3c-95c4-4833df2ab0bf', '2023-08-12 14:23:44.291297');