﻿using System.Collections.Generic;
using System.Threading.Tasks;
using Quix.Redshift.Domain.TimeSeries.Models;

namespace Quix.Redshift.Domain.TimeSeries.Repositories
{
    /// <summary>
    /// Interface to persist Quix.Sdk.Process models into time series database.
    /// </summary>
    public interface ITimeSeriesWriteRepository
    {
        /// <summary>
        /// Write batch of <see cref="ParameterDataRow"/> into database.
        /// </summary>
        Task WriteTelemetryData(string topicId, IEnumerable<KeyValuePair<string, IEnumerable<ParameterDataRowForWrite>>> streamParameterData);

        
        /// <summary>
        /// Write batch of <see cref="ParameterDataRow"/> into database.
        /// </summary>
        Task WriteTelemetryEvent(string topicId, IEnumerable<KeyValuePair<string, IEnumerable<EventDataRow>>> streamEventData);
    }
}