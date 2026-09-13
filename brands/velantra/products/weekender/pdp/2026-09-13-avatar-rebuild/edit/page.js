(() => {
  const init = () => {
    const section = document.querySelector('[data-wk-product]');
    if (!section || section.dataset.initialized) return;
    section.dataset.initialized = 'true';
    const q = selector => section.querySelector(selector);
    const qa = selector => Array.from(section.querySelectorAll(selector));
    const config = JSON.parse(q('[data-wk-config]').textContent);
    const format = value => new Intl.NumberFormat(config.locale, {style:'currency',currency:config.currency}).format(value / 100);
    const endpoint = name => config.root.replace(/\/$/, '') + '/' + name;
    const gallery = q('[data-wk-gallery]');
    const allImages = qa('[data-wk-image]');
    let activeImages = [], photoIndex = 0, busy = false;
    let variant = config.variants.find(v => String(v.id) === q('[data-wk-variant-input]').value) || config.variants[0];
    const lightbox = q('[data-wk-lightbox]');
    const cart = q('[data-wk-cart]');
    const form = q('.wk-product-form');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const request = async (url, options={}) => {
      const response = await (window.wkEditorialFetch || window.fetch.bind(window))(endpoint(url) + '?wk_editorial=1', {...options, headers:{'Accept':'application/json','Content-Type':'application/json',...options.headers}});
      const data = await response.json();
      if (!response.ok) throw new Error(data.description || data.message || config.error);
      return data;
    };
    const error = (node, message) => {node.textContent = message;node.hidden = !message;};
    const updateCounter = () => {q('[data-wk-image-counter]').textContent = `${photoIndex + 1} / ${activeImages.length}`;};
    const showPhoto = (index, zoom=false) => {
      photoIndex = (index + activeImages.length) % activeImages.length;
      const photo = activeImages[photoIndex];
      if (!photo) return;
      updateCounter();
      if (zoom) {
        const img = photo.querySelector('img');
        q('[data-wk-lightbox-image]').src = img.src;
        q('[data-wk-lightbox-image]').alt = img.alt;
        q('[data-wk-lightbox-caption]').textContent = photo.dataset.caption;
        if (!lightbox.open) lightbox.showModal();
      } else if (matchMedia('(max-width:749px)').matches) {
        gallery.scrollTo({left:photo.offsetLeft - activeImages[0].offsetLeft,behavior:reduced?'instant':'smooth'});
      } else showPhoto(photoIndex, true);
    };
    const syncVariant = (writeUrl=true) => {
      const black = variant.option1 === 'Black';
      const preorder = black && section.dataset.blackPreorder === 'true';
      q('[data-wk-variant-input]').value = variant.id;
      q('[data-wk-color-name]').textContent = variant.option1;
      q('[data-wk-sticky-color]').textContent = variant.option1;
      q('[data-wk-price]').textContent = format(variant.price) + ' ' + config.currency;
      q('[data-wk-sticky-price]').textContent = format(variant.price);
      q('[data-wk-compare]').textContent = format(variant.compare_at_price || 0);
      q('[data-wk-compare]').hidden = q('[data-wk-sale]').hidden = !(variant.compare_at_price > variant.price);
      qa('[data-wk-add],[data-wk-sticky-add]').forEach(button => {
        button.disabled = !variant.available || busy;
        button.textContent = busy ? config.adding : !variant.available ? config.soldOut : preorder ? config.preorder : config.add;
      });
      q('[data-wk-material]').textContent = black ? config.leather : config.canvas;
      q('[data-wk-detail-material]').textContent = black ? config.leatherDetail : config.canvasDetail;
      q('[data-wk-preorder-detail]').hidden = !preorder;
      q('[data-wk-offer-body]').textContent = variant.compare_at_price > variant.price ? config.saveTemplate.replace('__AMOUNT__',format(variant.compare_at_price-variant.price)) : config.regularOffer;
      allImages.forEach(image => {image.hidden = image.dataset.color !== variant.option1;});
      activeImages = allImages.filter(image => !image.hidden);
      photoIndex = 0;gallery.scrollLeft = 0;updateCounter();
      if (writeUrl) {const url = new URL(location.href);url.searchParams.set('variant',variant.id);history.replaceState({},'',url);}
    };
    syncVariant(false);
    qa('[data-wk-color-radio]').forEach(radio => radio.addEventListener('change',() => {
      const selected = config.variants.find(v=>String(v.id)===radio.value);
      if (selected) {variant = selected;syncVariant();}
    }));
    allImages.forEach(item=>item.addEventListener('click',()=>showPhoto(activeImages.indexOf(item),true)));
    q('[data-wk-prev]').addEventListener('click',()=>showPhoto(photoIndex-1));
    q('[data-wk-next]').addEventListener('click',()=>showPhoto(photoIndex+1));
    q('[data-wk-lightbox-prev]').addEventListener('click',()=>showPhoto(photoIndex-1,true));
    q('[data-wk-lightbox-next]').addEventListener('click',()=>showPhoto(photoIndex+1,true));
    q('[data-wk-lightbox-close]').addEventListener('click',()=>lightbox.close());
    lightbox.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'){event.preventDefault();showPhoto(photoIndex-1,true);}if(event.key==='ArrowRight'){event.preventDefault();showPhoto(photoIndex+1,true);}});
    gallery.addEventListener('scroll',()=>{if(matchMedia('(max-width:749px)').matches){photoIndex=Math.min(activeImages.length-1,Math.max(0,Math.round(gallery.scrollLeft/gallery.clientWidth)));updateCounter();}},{passive:true});
    const businessDays = (date, days) => {const out = new Date(date);let left=days;while(left>0){out.setUTCDate(out.getUTCDate()+1);if(out.getUTCDay()!==0&&out.getUTCDay()!==6)left--;}return out;};
    if(section.dataset.country==='US') {
      const dateParts = new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
      const part = name=>dateParts.find(p=>p.type===name).value;
      const dispatch = new Date(`${part('year')}-${part('month')}-${part('day')}T12:00:00Z`);
      dispatch.setUTCDate(dispatch.getUTCDate()+Number(section.dataset.dispatch));
      const dateFormat = new Intl.DateTimeFormat(config.locale,{month:'short',day:'numeric',timeZone:'UTC'});
      const min = dateFormat.format(businessDays(dispatch,Number(section.dataset.transitMin)));
      const max = dateFormat.format(businessDays(dispatch,Number(section.dataset.transitMax)));
      q('[data-wk-arrival]').textContent = config.orderToday.replace('__MIN__',min).replace('__MAX__',max);
    } else q('[data-wk-arrival]').textContent = config.international;
    document.querySelectorAll('a[href="#wk-review-form"]').forEach(link=>link.addEventListener('click',()=>{q('#wk-review-form').open=true;}));
    if(location.hash==='#wk-review-form'||location.hash==='#wk-review-contact')q('#wk-review-form').open=true;
    new IntersectionObserver(entries=>{q('[data-wk-sticky]').hidden = entries[0].isIntersecting;},{threshold:0}).observe(q('[data-wk-add]'));
    const element = (tag, className, text) => {const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=text;return node;};
    const renderCart = data => {
      const container = q('[data-wk-cart-items]');container.replaceChildren();
      document.querySelectorAll('[data-wk-cart-count]').forEach(node=>{node.textContent=data.item_count;});
      if(!data.items.length) container.append(element('p','',config.empty));
      data.items.forEach(item=>{
        const card=element('article','wk-cart-item');
        const itemVariant=config.variants.find(v=>v.id===item.variant_id);
        const matching=itemVariant ? allImages.find(i=>i.dataset.color===itemVariant.option1) : null;
        const thumb=element('img');thumb.alt=item.product_title;thumb.src=matching?matching.querySelector('img').src:item.image;thumb.width=80;thumb.height=100;
        const info=element('div');info.append(element('h3','',item.product_title),element('p','',`${item.variant_title || ''} · ${config.quantity} ${item.quantity}`),element('p','',format(item.final_line_price)));
        const remove=element('button','',config.remove);remove.type='button';remove.addEventListener('click',async()=>{remove.disabled=true;try{renderCart(await request('cart/change.js',{method:'POST',body:JSON.stringify({id:item.key,quantity:0})}));}catch(e){error(q('[data-wk-cart-error]'),e.message);remove.disabled=false;}});info.append(remove);card.append(thumb,info);container.append(card);
      });
      q('[data-wk-cart-total]').textContent=format(data.total_price);
      q('[data-wk-checkout]').disabled=!data.item_count;
    };
    const openCart = async () => {
      error(q('[data-wk-cart-error]'),'');
      try{renderCart(await request('cart.js'));if(!cart.open)cart.showModal();}catch(e){if(!cart.open)cart.showModal();error(q('[data-wk-cart-error]'),e.message);}
    };
    document.querySelectorAll('[data-wk-cart-open]').forEach(button=>button.addEventListener('click',openCart));
    qa('[data-wk-cart-close]').forEach(button=>button.addEventListener('click',()=>cart.close()));
    form.addEventListener('submit',async event=>{
      event.preventDefault();if(busy||!variant.available)return;busy=true;
      qa('[data-wk-add],[data-wk-sticky-add]').forEach(button=>{button.disabled=true;button.textContent=config.adding;});
      error(q('[data-wk-product-error]'),'');
      try{await request('cart/add.js',{method:'POST',body:JSON.stringify({items:[{id:variant.id,quantity:1}]})});await openCart();}catch(e){error(q('[data-wk-product-error]'),e.message);}finally{busy=false;qa('[data-wk-add],[data-wk-sticky-add]').forEach(button=>{button.disabled=!variant.available;button.textContent=!variant.available?config.soldOut:variant.option1==='Black'&&section.dataset.blackPreorder==='true'?config.preorder:config.add;});}
    });
    document.addEventListener('shopify:section:load',init,{once:true});
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
