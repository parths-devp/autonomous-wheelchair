# Steering mechanism CAD

This directory is for the castor-wheel steering assembly, linkage, gears, shaft, and NEMA 17 motor mount.

## Design details recorded during development

- Two castor wheels, approximately 300 g each.
- The two wheel assemblies are connected through a shaft arrangement; a 120 mm shaft dimension was discussed.
- Steering actuation uses a NEMA 17 stepper motor and a pair of printed gears.
- Gear outside diameter discussed: 120 mm.
- Gear face width: 15 mm.
- Gear material: PLA.
- Print process: Bambu FDM printer.
- Infill: 15% rectilinear.
- Linkage angle used in the torque calculation: 65 degrees.
- The pivot is offset from the wheel centre; the pivot-to-outer-face dimension discussed was 40 mm.

Treat these as design inputs from the prototype discussion, not as a complete released drawing. Confirm each dimension against the latest CAD model before manufacturing or using it in strength calculations.

## Files to add

Include the native Fusion 360 design, STEP export, gear drawings, linkage dimensions, shaft dimensions, motor mounting details, and a calculation sheet covering torque, tooth strength, shaft loading, and printed-part limitations.

PLA printed gears are sensitive to temperature, layer orientation, infill, and impact. The current print settings alone do not establish a safe load rating.