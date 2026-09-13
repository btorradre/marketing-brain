"""Colette-only prompt refinement; existing approved Omni transport unchanged."""
import importlib.util
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'generate_film.py'
s=importlib.util.spec_from_file_location('colette_approved_generation',p)
generation=importlib.util.module_from_spec(s);s.loader.exec_module(generation)
original=generation.prompt
def prompt(job,stage):
    text=original(job,stage)
    if stage==2:
        text=text.replace('[2-3.75s] Hard cut to a complete bag portrait matching Image1 literally, including its exact two handles and closure state. Center it in the safe box with a tiny axial pullback.', '[2-3.75s] Hard cut to an extreme close-up of only the pale OATMEAL FELT front body, matching Image3 literally. Pale short fuzzy fibers and heathered felt completely fill the frame. No handles, leather, belt, gold caps, seams or body edges appear in this texture-only shot. Minute lateral camera glide.')
        text=text.replace("[7.25-9s] Hard cut to a final complete-bag portrait matching Image1's angle, source shape and state literally. Both handles and the entire bag fit comfortably within the central46percent of width and76percent of height. Quiet axial camera pullback until the final frame. No fade, title or endcard.", "[7.25-9s] Hard cut to the EXACT Image1 complete-bag three-quarter portrait again. Image1 literally supplies the entire final composition: pale OATMEAL FELT body, pale FELT lower handle legs and pale FELT vertical front strips, with only the upper handle arcs and narrow front belt in Caramel leather. Both handle arches have the exact height, spacing and front/rear overlap of Image1; preserve the shown right gusset and two separate curved hanging belt ends with one gold cap each. The body MUST remain pale felt, never brown leather. Keep every handle and body corner comfortably inside central46percent of width and76percent of height. Stationary camera, very subtle natural focus breathing only, no turn or new angle. Finish on this original pale felt bag; no fade, title or endcard.")
        text+=' CRITICAL MATERIAL LOCK: this is an oatmeal FELT bag. Caramel leather exists only as narrow trims and upper handle wraps, never the body or full handle legs. Reference Image1 is the exact final product photograph, not a loose style inspiration.'
    return text
generation.prompt=prompt
if __name__=='__main__':generation.main()
