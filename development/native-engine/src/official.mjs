import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import * as THREE from "three";
import { createMotionRuntime } from "./motion-runtime.mjs";
export { gsap, ScrollTrigger, THREE };
export function createBrowserRuntime(options={}){return createMotionRuntime({gsap,ScrollTrigger,Lenis,document,mediaQuery:window.matchMedia("(prefers-reduced-motion: reduce)"),Observer:window.IntersectionObserver,...options})}
