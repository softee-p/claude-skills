# mapcn Component Reference

mapcn is a React component library for interactive maps built on MapLibre GL, styled with Tailwind CSS, and compatible with shadcn/ui. Free CARTO basemap tiles by default — no API key required. Automatic light/dark theme switching.

**Prerequisites:** Tailwind CSS + shadcn/ui configured in the project.

---

## Installation

### Base Map Component
```bash
npx shadcn@latest add @mapcn/map
```
Installs `maplibre-gl` dependency and adds the map component to `components/ui/map`.

### Additional Components
```bash
npx shadcn@latest add @mapcn/controls
npx shadcn@latest add @mapcn/marker
npx shadcn@latest add @mapcn/popup
npx shadcn@latest add @mapcn/route
npx shadcn@latest add @mapcn/cluster
```

All components import from `@/components/ui/map`.

---

## Map (Root Container)

Initializes MapLibre GL and provides context to all child map components.

```tsx
import { Map, MapControls } from "@/components/ui/map";
import { Card } from "@/components/ui/card";

export function MyMap() {
  return (
    <Card className="h-[320px] p-0 overflow-hidden">
      <Map center={[-74.006, 40.7128]} zoom={11}>
        <MapControls />
      </Map>
    </Card>
  );
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Child components (markers, popups, controls, routes) |
| `className` | `string` | — | CSS classes for map container |
| `theme` | `"light" \| "dark"` | auto | Map theme; auto-detects from system |
| `styles` | `{ light?: string \| StyleSpecification; dark?: string \| StyleSpecification }` | CARTO tiles | Custom map styles (MapLibre GL style URLs) |
| `projection` | `ProjectionSpecification` | — | Map projection; use `{ type: "globe" }` for 3D |
| `viewport` | `Partial<MapViewport>` | — | Controlled viewport state |
| `onViewportChange` | `(viewport: MapViewport) => void` | — | Fires during pan/zoom/rotate |
| `loading` | `boolean` | `false` | Show loading indicator |
| `center` | `[number, number]` | — | `[longitude, latitude]` |
| `zoom` | `number` | — | Zoom level |

Extends `MapOptions` from MapLibre GL (excludes `container` and `style`). Additional MapLibre props like `maxBounds`, `minZoom`, `maxZoom`, `bearing`, `pitch` are passed through.

### MapViewport Type
```ts
interface MapViewport {
  center: [number, number]; // [lng, lat]
  zoom: number;
  bearing: number;          // rotation in degrees
  pitch: number;            // tilt in degrees
}
```

### Controlled Mode
```tsx
const [viewport, setViewport] = useState<Partial<MapViewport>>({
  center: [-74.006, 40.7128],
  zoom: 12,
});

<Map viewport={viewport} onViewportChange={setViewport} />
```

### Custom Styles
```tsx
<Map
  styles={{
    light: "https://tiles.openfreemap.org/styles/bright",
    dark: "https://tiles.openfreemap.org/styles/dark",
  }}
/>
```

---

## useMap Hook

Access the MapLibre map instance. Must be used within a `<Map>` component.

```tsx
import { useMap } from "@/components/ui/map";

function MyComponent() {
  const { map, isLoaded } = useMap();
  // map: MapLibre.Map instance
  // isLoaded: boolean
}
```

---

## MapControls

Interactive zoom, compass, locate, and fullscreen buttons.

**Install:** `npx shadcn@latest add @mapcn/controls`

```tsx
import { MapControls } from "@/components/ui/map";

<Map center={[2.3522, 48.8566]} zoom={11}>
  <MapControls
    position="bottom-right"
    showZoom
    showCompass
    showLocate
    showFullscreen
  />
</Map>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `position` | `"top-left" \| "top-right" \| "bottom-left" \| "bottom-right"` | `"bottom-right"` | Control position |
| `showZoom` | `boolean` | `true` | Zoom in/out buttons |
| `showCompass` | `boolean` | `false` | Compass reset button |
| `showLocate` | `boolean` | `false` | User location button |
| `showFullscreen` | `boolean` | `false` | Fullscreen toggle |
| `className` | `string` | — | CSS classes |
| `onLocate` | `(coords: { longitude: number; latitude: number }) => void` | — | Callback with user coordinates |

---

## MapMarker

Container for marker-related components. DOM-based — works best for up to a few hundred markers. For large datasets, use `MapClusterLayer`.

**Install:** `npx shadcn@latest add @mapcn/marker`

```tsx
import {
  MapMarker,
  MarkerContent,
  MarkerPopup,
  MarkerTooltip,
  MarkerLabel,
} from "@/components/ui/map";

<Map center={[-74.006, 40.7128]} zoom={12}>
  <MapMarker longitude={-74.006} latitude={40.7128}>
    <MarkerContent>
      <div className="h-4 w-4 rounded-full bg-blue-500 border-2 border-white" />
    </MarkerContent>
    <MarkerTooltip>
      <span>New York City</span>
    </MarkerTooltip>
    <MarkerPopup closeButton className="w-62">
      <div className="space-y-2">
        <h3 className="font-semibold">New York City</h3>
        <p className="text-sm text-muted-foreground">Population: 8.3M</p>
      </div>
    </MarkerPopup>
  </MapMarker>
</Map>
```

### MapMarker Props

| Prop | Type | Description |
|------|------|-------------|
| `longitude` | `number` | Marker longitude |
| `latitude` | `number` | Marker latitude |
| `children` | `ReactNode` | MarkerContent, MarkerPopup, MarkerTooltip, MarkerLabel |
| `onClick` | `(e: MouseEvent) => void` | Click handler |
| `onMouseEnter` | `(e: MouseEvent) => void` | Hover entry |
| `onMouseLeave` | `(e: MouseEvent) => void` | Hover exit |
| `onDragStart` | `(lngLat: {lng, lat}) => void` | Drag start (requires `draggable: true`) |
| `onDrag` | `(lngLat: {lng, lat}) => void` | During drag |
| `onDragEnd` | `(lngLat: {lng, lat}) => void` | Drag end |

Extends `MarkerOptions` from MapLibre GL (excludes `element`).

### MarkerContent Props

| Prop | Type | Description |
|------|------|-------------|
| `children` | `ReactNode` | Custom marker visual (defaults to blue dot if empty) |
| `className` | `string` | CSS classes |

### MarkerPopup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Popup content |
| `className` | `string` | — | CSS classes |
| `closeButton` | `boolean` | `false` | Show close button |

Extends `PopupOptions`. Popup styles are CSS-reset to prevent MapLibre style conflicts.

### MarkerTooltip Props

| Prop | Type | Description |
|------|------|-------------|
| `children` | `ReactNode` | Tooltip content |
| `className` | `string` | CSS classes |

Appears on hover, auto-dismisses on hover exit. Extends `PopupOptions`.

### MarkerLabel Props

Must be inside `MarkerContent`.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Label text |
| `className` | `string` | — | CSS classes |
| `position` | `"top" \| "bottom"` | `"top"` | Position relative to marker |

---

## MapPopup (Standalone)

Standalone popup placed anywhere on the map without a marker. Controlled programmatically.

**Install:** `npx shadcn@latest add @mapcn/popup`

```tsx
import { MapPopup } from "@/components/ui/map";

{showPopup && (
  <MapPopup
    longitude={-74.006}
    latitude={40.7128}
    onClose={() => setShowPopup(false)}
    closeButton
    focusAfterOpen={false}
    closeOnClick={false}
    className="w-62"
  >
    <div className="space-y-2">
      <h3 className="font-semibold">New York City</h3>
      <p className="text-sm text-muted-foreground">Population: 8.3 million</p>
    </div>
  </MapPopup>
)}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `longitude` | `number` | — | Popup longitude |
| `latitude` | `number` | — | Popup latitude |
| `onClose` | `() => void` | — | Close callback |
| `children` | `ReactNode` | — | Popup content |
| `className` | `string` | — | CSS classes |
| `closeButton` | `boolean` | `false` | Show close button |
| `focusAfterOpen` | `boolean` | — | Focus after open |
| `closeOnClick` | `boolean` | — | Close on outside click |

---

## MapRoute

Draws lines/paths connecting coordinate points.

**Install:** `npx shadcn@latest add @mapcn/route`

```tsx
import { MapRoute } from "@/components/ui/map";

const route: [number, number][] = [
  [-74.006, 40.7128],
  [-73.9857, 40.7484],
  [-73.9772, 40.7527],
  [-73.9654, 40.7829],
];

<Map center={[-73.98, 40.75]} zoom={11.2}>
  <MapRoute coordinates={route} color="#3b82f6" width={4} opacity={0.8} />
</Map>
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | auto | Unique route layer identifier |
| `coordinates` | `[number, number][]` | — | Array of `[lng, lat]` pairs |
| `color` | `string` | `"#4285F4"` | Line color |
| `width` | `number` | `3` | Line width in pixels |
| `opacity` | `number` | `0.8` | Line opacity (0-1) |
| `dashArray` | `[number, number]` | — | Dash pattern `[length, gap]` |
| `onClick` | `() => void` | — | Click handler |
| `onMouseEnter` | `() => void` | — | Hover entry |
| `onMouseLeave` | `() => void` | — | Hover exit |
| `interactive` | `boolean` | `true` | Enable pointer cursor on hover |

Routes render in order — sort to control z-index. Works with external routing APIs (e.g., OSRM). Combine with MapMarker for start/end points.

---

## MapClusterLayer

Native MapLibre clustering that auto-groups/ungroups points based on zoom level. Use for large datasets instead of DOM-based markers.

**Install:** `npx shadcn@latest add @mapcn/cluster`

```tsx
import { MapClusterLayer } from "@/components/ui/map";

<Map center={[-100, 40]} zoom={3}>
  <MapClusterLayer<EarthquakeProperties>
    data="https://maplibre.org/maplibre-gl-js/docs/assets/earthquakes.geojson"
    clusterRadius={50}
    clusterMaxZoom={14}
    clusterColors={["#1d8cf8", "#6d5dfc", "#e23670"]}
    pointColor="#1d8cf8"
    onPointClick={(feature, coordinates) => {
      setSelectedPoint({ coordinates, properties: feature.properties });
    }}
  />
</Map>
```

### Props

Generic: `MapClusterLayer<T extends Record<string, any>>`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `string \| GeoJSON.FeatureCollection` | — | GeoJSON data or URL |
| `clusterMaxZoom` | `number` | `14` | Max zoom for clustering |
| `clusterRadius` | `number` | `50` | Cluster radius in pixels |
| `clusterColors` | `[string, string, string]` | `["#22c55e", "#eab308", "#ef4444"]` | Colors for `[small, medium, large]` |
| `clusterThresholds` | `[number, number]` | `[100, 750]` | Point count thresholds |
| `pointColor` | `string` | `"#3b82f6"` | Unclustered point color |
| `onPointClick` | `(feature: GeoJSON.Feature, coords: [number, number]) => void` | — | Point click handler |
| `onClusterClick` | `(clusterId: number, coords: [number, number], count: number) => void` | — | Cluster click; auto-zooms if undefined |

---

## Advanced Usage

Direct access to the underlying MapLibre GL instance for custom functionality beyond component abstractions.

### MapRef (via useRef)

Attach a ref to the Map component for programmatic control from event handlers or effects.

```tsx
import { useRef } from "react";
import { Map, type MapRef } from "@/components/ui/map";

function FlyToExample() {
  const mapRef = useRef<MapRef>(null);

  return (
    <>
      <button onClick={() => mapRef.current?.flyTo({ center: [-74, 40.7], zoom: 12 })}>
        Fly to NYC
      </button>
      <Map ref={mapRef} center={[0, 20]} zoom={2} />
    </>
  );
}
```

`MapRef` exposes the full MapLibre GL map instance. Key methods: `flyTo()`, `easeTo()`, `setCenter()`, `setZoom()`, `setBearing()`, `setPitch()`, `fitBounds()`, `getCenter()`, `getZoom()`.

### Event Handling via useMap Hook

Register event listeners inside child components using `useMap`:

```tsx
import { useMap } from "@/components/ui/map";
import { useEffect } from "react";

function ClickHandler() {
  const { map, isLoaded } = useMap();

  useEffect(() => {
    if (!isLoaded) return;
    const handleClick = (e: maplibregl.MapMouseEvent) => {
      console.log("Clicked:", e.lngLat);
    };
    map.on("click", handleClick);
    return () => { map.off("click", handleClick); };
  }, [map, isLoaded]);

  return null;
}

// Usage: <Map><ClickHandler /></Map>
```

Common events: `click`, `dblclick`, `mousemove`, `mouseenter`, `mouseleave`, `move`, `moveend`, `zoom`, `zoomend`, `pitch`, `rotate`, `load`, `idle`.

### Custom GeoJSON Layers

Add custom geographic data as styled layers directly on the MapLibre canvas:

```tsx
function ParkLayer() {
  const { map, isLoaded } = useMap();

  useEffect(() => {
    if (!isLoaded) return;

    map.addSource("parks", {
      type: "geojson",
      data: parksGeoJSON,
    });

    map.addLayer({
      id: "parks-fill",
      type: "fill",
      source: "parks",
      paint: {
        "fill-color": "#22c55e",
        "fill-opacity": 0.4,
      },
    });

    map.addLayer({
      id: "parks-outline",
      type: "line",
      source: "parks",
      paint: {
        "line-color": "#16a34a",
        "line-width": 2,
      },
    });

    return () => {
      map.removeLayer("parks-outline");
      map.removeLayer("parks-fill");
      map.removeSource("parks");
    };
  }, [map, isLoaded]);

  return null;
}
```

### Performance Notes

- **DOM-based markers** (`MapMarker`): Good for up to a few hundred markers. Each creates a DOM element.
- **GeoJSON layers** (via `useMap` or `MapClusterLayer`): Use WebGL rendering — significantly faster for hundreds or thousands of points.
- For large datasets, prefer `MapClusterLayer` or custom GeoJSON layers over `MapMarker`.

### Extension Ideas

The MapLibre GL API supports building: real-time location tracking, geofencing with area triggers, heatmap visualizations, drawing tools (polygons/lines), 3D building extrusion, route animations, custom data overlays (weather, traffic, satellite). Consult the MapLibre GL JS documentation for the full methods and events API.

---

## Blocks (Pre-built Templates)

Blocks are full-featured, ready-to-use map views.

### Analytics Map
```bash
npx shadcn@latest add @mapcn/analytics-map
```
Real-time analytics overview: world map with breakdown cards, device stats, global user distribution, pages, referrers, countries, browser analytics.

### Logistics Network
```bash
npx shadcn@latest add @mapcn/logistics-network
```
Domestic logistics map with sidebar containing statistical information for tracking operations.

### Heatmap
```bash
npx shadcn@latest add @mapcn/heatmap
```
Globe-projected heatmap (e.g., earthquake density) with zoom-dependent styling.

### Delivery Tracker
```bash
npx shadcn@latest add @mapcn/delivery-tracker
```
Live order tracking: route progress, courier position, order details.
