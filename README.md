# EERL
Efficient Evolutionary Reinforcement Learning Algorithms


This repo contains genetic rl with reproduction reward also.



RL WTH GAN
https://github.com/ghliu/pytorch-ddpg
https://github.com/eriklindernoren/PyTorch-GAN/blob/master/implementations/gan/gan.py 
politikadan çıkan aksiyon ve state ikilisin ganlara sok ve next state çıktısı al
bu çıktıyı kritiğa sok reward expectation t+1 al
politikadan çıkan aksiyonu kritiğe sok reward exp t al
if reard exp t reward exp t+1 ile yakınsa iş yap
değilse random hareket al


YENİ FİKİRLER

RL Ve Genetik iki ayrı networkün yönettiği ajanlar populasyonu oluştur.
Model based yaklaşımı çok basit tut. Bir network action ve state girdisi olsun, çıkışı next state ve reward olsun.
Tek modelli veya her ajan için ayrı model oluşturabilirsin.
Genetik ve politika tarafı üzerine biraz düşün ama model based tarafı aksiyon seçiminde kullanılabilir. Örnek: select action try it on model if it generates good reward take it, else try new action with genetic code or with prob of genetic code.

İlk Mimari Denemesi:
EVrimsel Pekiştirmeli ÖĞrenme algoritmasına model ekle. (Model BAsed Evolutionary Reinforcement Learning)

İkinci Mimari Denemesi:
Genetik Ve rl politikalarını ayır. Genetik politika sadece learning rate ve exploration prob çıktısı versin. rl politikayı bu paramaetrelerle güncelle. Rl politikaları erl algoritmasına sok. genetik politikayı sadece evrimsele sok.

Üçüncü Mimari Denemesi :

İkinci Mimariye model ekle.

