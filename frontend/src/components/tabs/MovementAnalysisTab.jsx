/**
 * MovementAnalysisTab.jsx
 * Shared by Athlete ("MovementAnalysis") and Coach ("MovementQuality") tabs.
 * Shows: pose overlay video, detected anomaly banners, kinematic angle bars.
 */
import React from 'react';
import { Video, AlertTriangle } from 'lucide-react';
import { getVideoSource, formatDateTime } from '../../hooks/useApi';

export default function MovementAnalysisTab({ latestAnalysis, predictionReport, athleteName }) {
  if (!latestAnalysis) {
    return (
      <div className="content-hero-card animate-fade-in">
        <div className="hero-accent-strip" />
        <h2 className="workspace-title">Movement Anomaly Detection</h2>
        <div className="placeholder-tab-content">
          <Video size={48} className="placeholder-tab-icon" />
          <p className="placeholder-tab-text">
            No video upload found. Upload a video in the Overview tab to view your movement parameters.
          </p>
        </div>
      </div>
    );
  }

  const metrics = latestAnalysis.metrics || {};

  // Extract numerical values to calculate dynamic bar widths and colors
  const parseVal = (str, fallback) => {
    if (!str) return fallback;
    const match = String(str).match(/([\d.]+)/);
    return match ? parseFloat(match[1]) : fallback;
  };

  const valgusDeg = parseVal(metrics.knee_valgus, 5.2);
  const hipDeg = parseVal(metrics.hip_stability, 1.8);
  const trunkDeg = parseVal(metrics.trunk_lean, 8.5);
  const flexDeg = parseVal(metrics.landing_mechanics, 42.0);
  const alignPct = parseVal(metrics.joint_alignment, 93.6);

  const angleItems = [
    {
      label: 'Knee Valgus',
      value: metrics.knee_valgus,
      degStr: `${valgusDeg.toFixed(1)}°`,
      statusText: valgusDeg > 12 ? 'High Valgus' : (valgusDeg > 7 ? 'Mild Valgus' : 'Optimal'),
      width: `${Math.min(100, Math.max(15, (valgusDeg / 20) * 100))}%`,
      cls: valgusDeg > 12 ? 'warning' : 'optimal',
    },
    {
      label: 'Hip Stability',
      value: metrics.hip_stability,
      degStr: `${hipDeg.toFixed(1)}° tilt`,
      statusText: hipDeg > 4 ? 'Instability' : 'Optimal',
      width: `${Math.min(100, Math.max(15, (hipDeg / 10) * 100))}%`,
      cls: hipDeg > 4 ? 'warning' : 'optimal',
    },
    {
      label: 'Trunk Lean',
      value: metrics.trunk_lean,
      degStr: `${trunkDeg.toFixed(1)}°`,
      statusText: trunkDeg > 16 ? 'Excessive Lean' : 'Safe Posture',
      width: `${Math.min(100, Math.max(15, (trunkDeg / 25) * 100))}%`,
      cls: trunkDeg > 16 ? 'warning' : 'optimal',
    },
    {
      label: 'Landing Mechanics',
      value: metrics.landing_mechanics,
      degStr: `${flexDeg.toFixed(1)}° flexion`,
      statusText: flexDeg < 35 ? 'Stiff Impact' : 'Optimal Flexion',
      width: `${Math.min(100, Math.max(15, (flexDeg / 90) * 100))}%`,
      cls: flexDeg < 35 ? 'warning' : 'optimal',
    },
    {
      label: 'Joint Alignment',
      value: metrics.joint_alignment,
      degStr: `${alignPct.toFixed(1)}%`,
      statusText: alignPct < 80 ? 'Asymmetric' : 'Symmetric',
      width: `${Math.min(100, Math.max(20, alignPct))}%`,
      cls: alignPct < 80 ? 'warning' : 'optimal',
    },
  ];

  const processedDateStr = formatDateTime(latestAnalysis.upload_date || latestAnalysis.created_at);

  return (
    <div className="content-hero-card animate-fade-in">
      <div className="hero-accent-strip" />
      <h2 className="workspace-title">Movement Anomaly Detection</h2>
      <p className="workspace-desc">
        Computer vision joint angle tracking feedback &amp; anomaly detection engine output.
      </p>

      <div className="athlete-detail-view animate-scale-in">
        {/* Pose overlay video */}
        {latestAnalysis.video_url && (
          <div className="video-player-card" style={{ marginBottom: 20, backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 8 }}>
              <h3 style={{ margin: 0, fontSize: '1.15rem', fontWeight: 800 }}>Biomechanical Pose Tracking Video</h3>
              {processedDateStr && (
                <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                  📅 Processed: {processedDateStr}
                </span>
              )}
            </div>
            <video
              key={latestAnalysis.video_url || latestAnalysis.analysis_id}
              src={getVideoSource(latestAnalysis.video_url)}
              controls
              playsInline
              style={{ width: '100%', maxWidth: 720, borderRadius: 8, border: '1px solid var(--border-color)', backgroundColor: '#000', display: 'block' }}
            />
          </div>
        )}

        {/* Anomaly banners */}
        {predictionReport?.anomalies?.length > 0 && (
          <div className="anomalies-section" style={{ marginBottom: 24 }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 12 }}>Detected Movement Flaws &amp; Anomalies</h3>
            <div className="anomalies-grid" style={{ display: 'grid', gap: 12 }}>
              {predictionReport.anomalies.map((anom, idx) => (
                <div key={idx} style={{ padding: 16, borderRadius: 8, border: '1px solid var(--border-color)', backgroundColor: 'var(--bg-surface)', display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <AlertTriangle size={20} color={anom.severity === 'Critical' ? '#ef4444' : '#f59e0b'} style={{ marginTop: 2 }} />
                  <div>
                    <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 700 }}>
                      {anom.title}{' '}
                      <span style={{ fontSize: '0.75rem', padding: '2px 6px', borderRadius: 4, backgroundColor: anom.severity === 'Critical' ? '#fef2f2' : '#fffbeb', color: anom.severity === 'Critical' ? '#dc2626' : '#d97706', marginLeft: 8 }}>
                        {anom.severity}
                      </span>
                    </h4>
                    <p style={{ margin: '4px 0 0', fontSize: '0.85rem', color: 'var(--text-muted)' }}>{anom.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Kinematic angle bars */}
        <div className="joint-angles-card" style={{ padding: 24, backgroundColor: 'var(--bg-surface)', border: '1px solid var(--border-color)', borderRadius: 12 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, flexWrap: 'wrap', gap: 8 }}>
            <div>
              <h3 style={{ margin: '0 0 4px', fontSize: '1.1rem', fontWeight: 800 }}>Pose Estimation Kinematic Angles</h3>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Source file: {latestAnalysis.filename}</span>
            </div>
            {processedDateStr && (
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                📅 {processedDateStr}
              </span>
            )}
          </div>
          <div className="angles-grid-clean" style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {angleItems.map(({ label, value, degStr, statusText, width, cls }) => value ? (
              <div key={label} style={{ padding: '14px 18px', backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-color)', borderRadius: 8, display: 'flex', flexDirection: 'column', gap: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <span style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>{label}</span>
                    <span style={{
                      fontSize: '0.72rem', fontWeight: 700, padding: '2px 8px', borderRadius: 6,
                      backgroundColor: cls === 'warning' ? '#fef3c7' : '#dcfce7',
                      color: cls === 'warning' ? '#b45309' : '#15803d',
                      border: cls === 'warning' ? '1px solid #fde68a' : '1px solid #bbf7d0'
                    }}>
                      {statusText}
                    </span>
                  </div>
                  <span style={{ fontSize: '0.9rem', fontWeight: 800, color: cls === 'warning' ? '#d97706' : '#10b981' }}>
                    {degStr}
                  </span>
                </div>

                <div style={{ width: '100%', height: 7, backgroundColor: 'var(--bg-card, #e2e8f0)', borderRadius: 4, overflow: 'hidden' }}>
                  <div
                    style={{
                      width,
                      height: '100%',
                      backgroundColor: cls === 'warning' ? '#f59e0b' : '#10b981',
                      borderRadius: 4,
                      transition: 'width 0.5s ease'
                    }}
                  />
                </div>

                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>
                  {value}
                </div>
              </div>
            ) : null)}
          </div>
        </div>
      </div>
    </div>
  );
}
