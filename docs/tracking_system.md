# Shipment Tracking System Documentation

## Overview
The shipment tracking system provides real-time tracking capabilities for Segecha Logistics shipments, including route visualization, location updates, and estimated delivery times.

## Features

### Map Display
- Interactive map using Leaflet.js and OpenStreetMap
- Custom markers for pickup, delivery, and current locations
- Real-time route visualization
- Distance and time estimation
- Animated current location marker

### Route Calculation
```javascript
// Route calculation using OSRM
const response = await fetch(`https://router.project-osrm.org/route/v1/driving/${pickup[1]},${pickup[0]};${dropoff[1]},${dropoff[0]}?overview=full&geometries=polyline`);
```

### Marker Types
1. Pickup Location Marker
   - Blue circular marker
   - Shows pickup address in popup
   - Fixed position

2. Delivery Location Marker
   - Green circular marker
   - Shows delivery address in popup
   - Fixed position

3. Current Location Marker
   - Animated blue marker
   - Pulsing effect
   - Updates with shipment location
   - Shows current location details

### Route Display
- Blue polyline showing the route
- 4px width for visibility
- 0.7 opacity for style
- Popup showing:
  - Total distance in kilometers
  - Estimated time in hours

## Implementation Details

### Map Initialization
```javascript
const map = L.map('map', {
    minZoom: 2,
    maxZoom: 18
}).setView([0, 35], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18
}).addTo(map);
```

### Marker Creation
```javascript
const marker = L.marker(coordinates, {
    icon: L.divIcon({
        className: 'custom-div-icon',
        html: '<div style="background-color: #3B82F6; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.3);"></div>',
        iconSize: [12, 12]
    })
});
```

### Route Polyline
```javascript
const routeLayer = L.polyline(coordinates, {
    color: '#3B82F6',
    weight: 4,
    opacity: 0.7,
    lineJoin: 'round'
});
```

## Styling

### Map Container
```css
#map {
    height: 400px;
    width: 100%;
    background: #f8f9fa;
}
```

### Current Location Animation
```css
.current-location-marker {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
}
```

## Error Handling

### Map Initialization
```javascript
try {
    // Map initialization code
} catch (error) {
    console.error('Error initializing map:', error);
}
```

### Route Fetching
```javascript
try {
    const response = await fetch(routeUrl);
    const data = await response.json();
    // Route processing
} catch (error) {
    console.error('Error fetching route:', error);
}
```

## Future Improvements

1. Real-time Updates
   - WebSocket integration for live location updates
   - Automatic route recalculation
   - ETA updates

2. Enhanced Route Display
   - Multiple route options
   - Traffic information
   - Alternative routes

3. Additional Features
   - Geofencing alerts
   - Route optimization
   - Weather overlay
   - Traffic updates

## Maintenance

### Regular Tasks
1. Check OSRM service status
2. Monitor map tile usage
3. Update marker styles
4. Review error logs
5. Update route calculation parameters

### Troubleshooting
1. Grey map: Check tile server connection
2. Missing route: Verify OSRM service
3. Marker issues: Check coordinate validity
4. Animation problems: Review CSS compatibility 