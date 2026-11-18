import {mount as mount_ATZ_NAV_001} from "/ATREZZO-STUDIOS-AI/public/preview/v07/components/navegacion/ATZ-NAV-001.js";
import {mount as mount_ATZ_MIC_003} from "/ATREZZO-STUDIOS-AI/public/preview/v07/components/microinteractions/ATZ-MIC-003.js";
import {mount as mount_ATZ_MOT_002} from "/ATREZZO-STUDIOS-AI/public/preview/v07/components/motion/ATZ-MOT-002.js";
import {mount as mount_ATZ_MOT_003} from "/ATREZZO-STUDIOS-AI/public/preview/v07/components/motion/ATZ-MOT-003.js";
import {mount as mount_ATZ_MOT_006} from "/ATREZZO-STUDIOS-AI/public/preview/v07/components/motion/ATZ-MOT-006.js";
import {mount as mount_ATZ_MOT_008} from "/ATREZZO-STUDIOS-AI/public/preview/v07/components/typography/ATZ-MOT-008.js";
const mounts=[["ATZ-MOT-008",mount_ATZ_MOT_008],["ATZ-NAV-001",mount_ATZ_NAV_001],["ATZ-MIC-003",mount_ATZ_MIC_003],["ATZ-MOT-002",mount_ATZ_MOT_002],["ATZ-MOT-003",mount_ATZ_MOT_003],["ATZ-MOT-006",mount_ATZ_MOT_006]];
const done=new Map();function init(){for(const [root,controller] of done){if(!root.isConnected){controller?.destroy?.();done.delete(root)}}for(const [id,mount] of mounts){for(const root of document.querySelectorAll(`[data-atz-id="${id}"]`)){if(done.has(root))continue;try{done.set(root,mount(root))}catch(e){console.error(id,e)}}}}
init();const obs=new MutationObserver(init);obs.observe(document.getElementById("experience"),{childList:true,subtree:true});
